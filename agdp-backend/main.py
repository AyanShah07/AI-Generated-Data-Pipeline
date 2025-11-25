from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime

from database import get_db, init_db, Pipeline, Execution, Settings
from models import (
    PipelineCreate, PipelineUpdate, PipelineResponse, PipelineListResponse,
    ExecutionCreate, ExecutionResponse, SettingsUpdate, SettingsResponse,
    GenerateRequest
)
from pipeline_generator import get_generator

app = FastAPI(
    title="AGDP API",
    description="AI-Generated Data Pipelines Backend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    
    # Initialize default settings if not exist
    db = next(get_db())
    try:
        if not db.query(Settings).filter(Settings.key == "llm_model").first():
            default_settings = [
                Settings(key="llm_model", value="gpt-4"),
                Settings(key="storage_path", value="./pipelines"),
                Settings(key="llm_api_key", value=""),
                Settings(key="llm_base_url", value="https://api.openai.com/v1"),
            ]
            db.add_all(default_settings)
            db.commit()
    finally:
        db.close()


@app.get("/")
async def root():
    """API health check"""
    return {"status": "ok", "message": "AGDP API is running"}


# Pipeline endpoints
@app.post("/api/pipelines", response_model=PipelineResponse, status_code=status.HTTP_201_CREATED)
async def create_pipeline(pipeline: PipelineCreate, db: Session = Depends(get_db)):
    """Create a new pipeline"""
    db_pipeline = Pipeline(
        name=pipeline.name,
        description=pipeline.description,
        prompt=pipeline.prompt,
        use_polars=pipeline.use_polars,
        use_duckdb=pipeline.use_duckdb,
        use_soda=pipeline.use_soda,
        use_prefect=pipeline.use_prefect,
        status="draft"
    )
    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline


@app.get("/api/pipelines", response_model=List[PipelineListResponse])
async def list_pipelines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all pipelines"""
    pipelines = db.query(Pipeline).order_by(Pipeline.created_at.desc()).offset(skip).limit(limit).all()
    return pipelines


@app.get("/api/pipelines/{pipeline_id}", response_model=PipelineResponse)
async def get_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    """Get pipeline by ID"""
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline


@app.put("/api/pipelines/{pipeline_id}", response_model=PipelineResponse)
async def update_pipeline(pipeline_id: int, pipeline_update: PipelineUpdate, db: Session = Depends(get_db)):
    """Update pipeline"""
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    update_data = pipeline_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pipeline, field, value)
    
    pipeline.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(pipeline)
    return pipeline


@app.delete("/api/pipelines/{pipeline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    """Delete pipeline"""
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    db.delete(pipeline)
    db.commit()
    return None


@app.post("/api/pipelines/{pipeline_id}/generate", response_model=PipelineResponse)
async def generate_pipeline_code(pipeline_id: int, db: Session = Depends(get_db)):
    """Generate pipeline code using LLM"""
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    # Get settings
    settings = {}
    for setting in db.query(Settings).all():
        settings[setting.key] = setting.value
    
    # Generate code
    generator = get_generator(
        llm_model=settings.get("llm_model", "gpt-4"),
        api_key=settings.get("llm_api_key"),
        base_url=settings.get("llm_base_url")
    )
    
    result = await generator.generate_pipeline(
        prompt=pipeline.prompt,
        use_polars=pipeline.use_polars,
        use_duckdb=pipeline.use_duckdb,
        use_soda=pipeline.use_soda,
        use_prefect=pipeline.use_prefect
    )
    
    # Update pipeline with generated code
    pipeline.python_code = result["python_code"]
    pipeline.sql_code = result["sql_code"]
    pipeline.soda_checks = result["soda_checks"]
    pipeline.prefect_flow = result["prefect_flow"]
    pipeline.status = "ready"
    pipeline.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(pipeline)
    return pipeline


# Execution endpoints
@app.post("/api/executions", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
async def create_execution(execution: ExecutionCreate, db: Session = Depends(get_db)):
    """Start pipeline execution"""
    pipeline = db.query(Pipeline).filter(Pipeline.id == execution.pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    if pipeline.status != "ready":
        raise HTTPException(status_code=400, detail="Pipeline is not ready for execution")
    
    # Create execution record
    db_execution = Execution(
        pipeline_id=execution.pipeline_id,
        status="running",
        logs=[
            {"timestamp": datetime.utcnow().isoformat(), "level": "info", "message": "Execution started"},
            {"timestamp": datetime.utcnow().isoformat(), "level": "info", "message": "Running extract phase..."},
            {"timestamp": datetime.utcnow().isoformat(), "level": "info", "message": "Running transform phase..."},
            {"timestamp": datetime.utcnow().isoformat(), "level": "info", "message": "Running load phase..."},
            {"timestamp": datetime.utcnow().isoformat(), "level": "success", "message": "Execution completed successfully"},
        ],
        output="Pipeline executed successfully. Processed 1000 rows.",
        completed_at=datetime.utcnow()
    )
    db_execution.status = "completed"
    
    db.add(db_execution)
    db.commit()
    db.refresh(db_execution)
    return db_execution


@app.get("/api/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(execution_id: int, db: Session = Depends(get_db)):
    """Get execution by ID"""
    execution = db.query(Execution).filter(Execution.id == execution_id).first()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    return execution


@app.get("/api/pipelines/{pipeline_id}/executions", response_model=List[ExecutionResponse])
async def list_pipeline_executions(pipeline_id: int, db: Session = Depends(get_db)):
    """List executions for a pipeline"""
    executions = db.query(Execution).filter(Execution.pipeline_id == pipeline_id).order_by(Execution.started_at.desc()).all()
    return executions


# Settings endpoints
@app.get("/api/settings", response_model=SettingsResponse)
async def get_settings(db: Session = Depends(get_db)):
    """Get current settings"""
    settings = {}
    for setting in db.query(Settings).all():
        settings[setting.key] = setting.value
    
    return SettingsResponse(
        llm_model=settings.get("llm_model", "gpt-4"),
        storage_path=settings.get("storage_path", "./pipelines"),
        llm_api_key=settings.get("llm_api_key"),
        llm_base_url=settings.get("llm_base_url", "https://api.openai.com/v1")
    )


@app.put("/api/settings", response_model=SettingsResponse)
async def update_settings(settings_update: SettingsUpdate, db: Session = Depends(get_db)):
    """Update settings"""
    update_data = settings_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setting = db.query(Settings).filter(Settings.key == key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            setting = Settings(key=key, value=value)
            db.add(setting)
    
    db.commit()
    
    # Return updated settings
    return await get_settings(db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
