from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Optional
import uuid
import pandas as pd
import logging
from ..models.data_models import DataUploadResponse
from ..utils.data_parsing import parse_financial_data
from . import data_store
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/data",
    tags=["Data Management"]
)
@router.post("", response_model=DataUploadResponse)
def upload_financial_data(
    asset_file: UploadFile = File(..., description="CSV or JSON file containing asset returns (dates as index, columns as assets)"),
    benchmark_file: Optional[UploadFile] = File(None, description="Optional CSV or JSON file containing benchmark returns (single column, dates as index)"),
    file_format: Optional[str] = Form(None, description="Format of the files ('csv' or 'json'). If omitted, attempts to infer from filename/content-type.")
):
    """
    Upload asset returns and optionally benchmark returns.
    The API will store the data temporarily and returns a unique data_id for use in the subequent optimization API calls.
    """
    logger.info(f"Received data upload request. Asset file: {asset_file.filename}, Benchmark file: {benchmark_file.filename if benchmark_file else 'None'}")
    try:
        logger.info(f"Parsing asset file: {asset_file.filename}")
        asset_df = parse_financial_data(asset_file, file_format)
        logger.info(f"Successfully parsed asset file. Shape: {asset_df.shape}")
    except HTTPException as e:
        logger.error(f"HTTPException during asset file parsing: {e.detail}", exc_info=True)
        raise HTTPException(status_code=e.status_code, detail=f"Asset file error: {e.detail}")
    except Exception as e:
        logger.exception(f"Unexpected error during asset file parsing: {asset_file.filename}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error parsing asset file: {str(e)}")
    
    benchmark_df: Optional[pd.DataFrame] = None
    benchmark_name: Optional[str] = None
    has_benchmark: bool = False
    if benchmark_file:
        try:
            logger.info(f"Parsing benchmark file: {benchmark_file.filename}")
            benchmark_df = parse_financial_data(benchmark_file, file_format)
            logger.info(f"Successfully parsed benchmark file. Shape: {benchmark_df.shape}")

            if len(benchmark_df.columns) != 1:
                logger.warning(f"Benchmark file {benchmark_file.filename} has {len(benchmark_df.columns)} columns, expected 1.")
                raise ValueError("Benchmark file must contain exactly one column.")

            logger.info("Aligning asset and benchmark indices.")
            common_index = asset_df.index.intersection(benchmark_df.index)
            if common_index.empty:
                 logger.warning("No overlapping dates found between asset and benchmark data.")
                 raise ValueError("Asset and Benchmark data have no overlapping dates.")

            asset_df = asset_df.loc[common_index]
            benchmark_df = benchmark_df.loc[common_index]
            logger.info(f"Data aligned to {len(common_index)} common dates. Asset shape: {asset_df.shape}, Benchmark shape: {benchmark_df.shape}")

            benchmark_name = benchmark_file.filename
            has_benchmark = True
        except HTTPException as e:
            logger.error(f"HTTPException during benchmark file parsing: {e.detail}", exc_info=True)
            raise HTTPException(status_code=e.status_code, detail=f"Benchmark file error: {e.detail}")
        except ValueError as e:
            logger.error(f"ValueError during benchmark processing: {str(e)}", exc_info=True)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Benchmark data validation error: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error during benchmark file parsing: {benchmark_file.filename}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error parsing benchmark file: {str(e)}")
    data_id = uuid.uuid4()
    logger.info(f"Generated data_id: {data_id}")
    try:
        logger.info(f"Storing dataframes for data_id {data_id} in memory.")
        data_store[data_id] = (asset_df.copy(), benchmark_df.copy() if benchmark_df is not None else None)
        logger.info(f"Successfully stored data for data_id {data_id}")
    except Exception as e:
        logger.exception(f"Failed to store dataframes in memory for data_id {data_id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to store data internally.")

    response_data = DataUploadResponse(
        data_id=data_id,
        assets=list(asset_df.columns),
        num_assets=len(asset_df.columns),
        num_dates=len(asset_df.index),
        has_benchmark=has_benchmark,
        benchmark_name=benchmark_name,
    )
    logger.info(f"Data upload successful for data_id {data_id}. Returning response.")
    return response_data 