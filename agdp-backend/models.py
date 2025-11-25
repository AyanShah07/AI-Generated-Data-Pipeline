from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PipelineCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    prompt: str = Field(..., min_length=10)
    use_polars: bool = False
    use_duckdb: bool = False
    use_soda: bool = False
    use_prefect: bool = False


class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    prompt: Optional[str] = None
    use_polars: Optional[bool] = None
    use_duckdb: Optional[bool] = None
    use_soda: Optional[bool] = None
    use_prefect: Optional[bool] = None
    schedule_enabled: Optional[bool] = None
    schedule_cron: Optional[str] = None


class PipelineResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    prompt: str
    use_polars: bool
    use_duckdb: bool
    use_soda: bool
    use_prefect: bool
    python_code: Optional[str]
    sql_code: Optional[str]
    soda_checks: Optional[str]
    prefect_flow: Optional[str]
    created_at: datetime
    updated_at: datetime
    status: str
    schedule_enabled: bool
    schedule_cron: Optional[str]

    class Config:
        from_attributes = True


class PipelineListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExecutionCreate(BaseModel):
    pipeline_id: int


class ExecutionResponse(BaseModel):
    id: int
    pipeline_id: int
    status: str
    logs: List[Dict[str, Any]]
    output: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class SettingsUpdate(BaseModel):
    llm_model: Optional[str] = None
    storage_path: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None


class SettingsResponse(BaseModel):
    llm_model: str
    storage_path: str
    llm_api_key: Optional[str]
    llm_base_url: Optional[str]


class GenerateRequest(BaseModel):
    pipeline_id: int
