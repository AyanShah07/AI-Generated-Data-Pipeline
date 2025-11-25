from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./agdp.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    prompt = Column(Text)
    
    # Feature toggles
    use_polars = Column(Boolean, default=False)
    use_duckdb = Column(Boolean, default=False)
    use_soda = Column(Boolean, default=False)
    use_prefect = Column(Boolean, default=False)
    
    # Generated artifacts
    python_code = Column(Text, nullable=True)
    sql_code = Column(Text, nullable=True)
    soda_checks = Column(Text, nullable=True)
    prefect_flow = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default="draft")  # draft, ready, running, completed, failed
    
    # Schedule
    schedule_enabled = Column(Boolean, default=False)
    schedule_cron = Column(String, nullable=True)


class Execution(Base):
    __tablename__ = "executions"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, index=True)
    status = Column(String, default="running")  # running, completed, failed
    logs = Column(JSON, default=list)
    output = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
