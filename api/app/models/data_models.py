from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class DataUploadResponse(BaseModel):
    data_id: uuid.UUID = Field(..., description="Unique identifier for the uploaded dataset.")
    assets: List[str] = Field(..., description="List of asset identifiers (column names) detected in the asset file.")
    num_assets: int = Field(..., description="Number of assets found.")
    num_dates: int = Field(..., description="Number of time periods (rows) found in the aligned data.")
    has_benchmark: bool = Field(..., description="Whether benchmark data was successfully uploaded and aligned.")
    benchmark_name: Optional[str] = Field(None, description="Filename of the uploaded benchmark file, if provided.") 