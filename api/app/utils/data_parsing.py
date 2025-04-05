import pandas as pd
from fastapi import UploadFile, HTTPException, status
from io import BytesIO, StringIO
from typing import Optional
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_financial_data(file: UploadFile, file_format: Optional[str]) -> pd.DataFrame:
    """Parsez an uploaded CSV or JSON file into a pandas DataFrame with a DatetimeIndex."""
    filename = file.filename
    content_type = file.content_type
    logger.info(f"Starting parsing for file: {filename}, content-type: {content_type}, specified format: {file_format}")
    fmt = file_format
    if not fmt:
        if filename and '.csv' in filename.lower():
            fmt = 'csv'
            logger.info("Inferred format: CSV (from filename)")
        elif filename and '.json' in filename.lower():
            fmt = 'json'
            logger.info("Inferred format: JSON (from filename)")
        elif content_type and 'csv' in content_type:
            fmt = 'csv'
            logger.info("Inferred format: CSV (from content-type)")
        elif content_type and 'json' in content_type:
            fmt = 'json'
            logger.info("Inferred format: JSON (from content-type)")
        else:
            logger.error(f"Could not infer file format for {filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Could not infer file format for '{filename}'. Specify 'csv' or 'json'."
            )

    try:
        contents = file.file.read()
        logger.info(f"Read {len(contents)} bytes from {filename}")
    except Exception as e:
        logger.exception(f"Failed to read file content for {filename}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to read file: {str(e)}")
    finally:
        file.file.close()

    try:
        logger.info(f"Attempting to parse {filename} as {fmt.upper()}")
        if fmt == 'csv':
            
            df = pd.read_csv(StringIO(contents.decode('utf-8')), index_col=0, dayfirst=True)
        elif fmt == 'json':
            
            try:
                
                df = pd.read_json(BytesIO(contents), orient='columns', convert_dates=False) 
            except ValueError:
                try:
                    df = pd.read_json(BytesIO(contents), orient='index', convert_dates=False)
                except ValueError:
                     df = pd.read_json(BytesIO(contents), orient='split', convert_dates=False)
        else:
             logger.error(f"Unsupported format '{fmt}' encountered unexpectedly.")
             raise ValueError(f"Unsupported format: {fmt}")

        # Ensure index is DatetimeIndex, trying dayfirst=True here too
        try:
            # Attempt conversion, inferring format but prioritizing day first
            df.index = pd.to_datetime(df.index, dayfirst=True, errors='raise')
            logger.info(f"Successfully converted index to DatetimeIndex for {filename}")
        except (ValueError, TypeError) as dt_err:
            logger.error(f"Failed to convert index to Datetime for {filename}. Error: {dt_err}", exc_info=True)
            raise ValueError(f"Index column could not be parsed as dates (tried dayfirst=True). Ensure dates are in a consistent, recognizable format. Error: {dt_err}")


        logger.info(f"Successfully parsed {filename} into DataFrame with shape {df.shape}")
        if df.empty:
            logger.warning(f"Parsing {filename} resulted in an empty DataFrame.")
            raise ValueError("Uploaded file resulted in an empty dataset.")
        if df.isnull().values.any():
             logger.warning(f"NaN values detected in {filename}. Consider cleaning data before upload.")
             # df = df.fillna(0) or df.dropna()

        return df

    except (ValueError, TypeError, pd.errors.EmptyDataError, UnicodeDecodeError) as e:
        logger.error(f"Parsing failed for {filename} as {fmt.upper()}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to parse '{filename}' as {fmt.upper()}: {str(e)}"
        )
    except Exception as e:
         logger.exception(f"An unexpected error occurred during parsing of {filename}")
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while parsing '{filename}': {str(e)}"
         ) 