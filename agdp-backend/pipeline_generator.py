import json
from typing import Dict, Optional


class PipelineGenerator:
    """
    Generates ETL/ELT pipeline code based on natural language prompts.
    This is a placeholder implementation. In production, integrate with
    OpenAI, Anthropic, or your preferred LLM provider.
    """
    
    def __init__(self, llm_model: str = "gpt-4", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.llm_model = llm_model
        self.api_key = api_key
        self.base_url = base_url
    
    async def generate_pipeline(
        self,
        prompt: str,
        use_polars: bool = False,
        use_duckdb: bool = False,
        use_soda: bool = False,
        use_prefect: bool = False
    ) -> Dict[str, Optional[str]]:
        """
        Generate pipeline artifacts based on the prompt and feature toggles.
        
        Returns:
            Dict with keys: python_code, sql_code, soda_checks, prefect_flow
        """
        
        # Build context for LLM
        features = []
        if use_polars:
            features.append("Polars")
        if use_duckdb:
            features.append("DuckDB SQL")
        if use_soda:
            features.append("Soda data quality checks")
        if use_prefect:
            features.append("Prefect flow orchestration")
        
        features_str = ", ".join(features) if features else "standard Python"
        
        # TODO: Replace with actual LLM API call
        # For now, return template code
        
        python_code = self._generate_python_code(prompt, use_polars, use_duckdb, use_prefect)
        sql_code = self._generate_sql_code(prompt, use_duckdb) if use_duckdb else None
        soda_checks = self._generate_soda_checks(prompt) if use_soda else None
        prefect_flow = self._generate_prefect_flow(prompt, use_polars) if use_prefect else None
        
        return {
            "python_code": python_code,
            "sql_code": sql_code,
            "soda_checks": soda_checks,
            "prefect_flow": prefect_flow
        }
    
    def _generate_python_code(self, prompt: str, use_polars: bool, use_duckdb: bool, use_prefect: bool) -> str:
        """Generate Python ETL code"""
        if use_polars:
            return f'''# Generated Pipeline: {prompt}
import polars as pl

def extract():
    """Extract data from source"""
    df = pl.read_csv("data/input.csv")
    return df

def transform(df: pl.DataFrame) -> pl.DataFrame:
    """Transform data"""
    # Apply transformations based on: {prompt}
    df = df.filter(pl.col("value") > 0)
    df = df.with_columns(
        (pl.col("value") * 2).alias("value_doubled")
    )
    return df

def load(df: pl.DataFrame):
    """Load data to destination"""
    df.write_parquet("data/output.parquet")

if __name__ == "__main__":
    data = extract()
    transformed = transform(data)
    load(transformed)
    print("Pipeline completed successfully!")
'''
        else:
            return f'''# Generated Pipeline: {prompt}
import pandas as pd

def extract():
    """Extract data from source"""
    df = pd.read_csv("data/input.csv")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform data"""
    # Apply transformations based on: {prompt}
    df = df[df["value"] > 0]
    df["value_doubled"] = df["value"] * 2
    return df

def load(df: pd.DataFrame):
    """Load data to destination"""
    df.to_parquet("data/output.parquet", index=False)

if __name__ == "__main__":
    data = extract()
    transformed = transform(data)
    load(transformed)
    print("Pipeline completed successfully!")
'''
    
    def _generate_sql_code(self, prompt: str, use_duckdb: bool) -> str:
        """Generate DuckDB SQL code"""
        return f'''-- Generated SQL Pipeline: {prompt}
-- DuckDB SQL for data transformation

CREATE TABLE source_data AS 
SELECT * FROM read_csv_auto('data/input.csv');

CREATE TABLE transformed_data AS
SELECT 
    *,
    value * 2 AS value_doubled
FROM source_data
WHERE value > 0;

COPY transformed_data TO 'data/output.parquet' (FORMAT PARQUET);
'''
    
    def _generate_soda_checks(self, prompt: str) -> str:
        """Generate Soda data quality checks"""
        return f'''# Soda Data Quality Checks
# Generated for: {prompt}

checks for transformed_data:
  - row_count > 0
  - missing_count(value) = 0
  - invalid_count(value) = 0:
      valid min: 0
  - duplicate_count(id) = 0
  - schema:
      fail:
        when required column missing: [id, value, value_doubled]
'''
    
    def _generate_prefect_flow(self, prompt: str, use_polars: bool) -> str:
        """Generate Prefect flow orchestration code"""
        lib = "polars as pl" if use_polars else "pandas as pd"
        return f'''# Prefect Flow: {prompt}
from prefect import flow, task
import {lib}

@task(name="Extract Data", retries=2)
def extract():
    """Extract data from source"""
    df = {"pl" if use_polars else "pd"}.read_csv("data/input.csv")
    return df

@task(name="Transform Data")
def transform(df):
    """Transform data"""
    # Apply transformations
    {"df = df.filter(pl.col('value') > 0)" if use_polars else "df = df[df['value'] > 0]"}
    return df

@task(name="Load Data")
def load(df):
    """Load data to destination"""
    df.write_parquet("data/output.parquet")
    return "Success"

@flow(name="ETL Pipeline")
def etl_pipeline():
    """Main ETL pipeline flow"""
    data = extract()
    transformed = transform(data)
    result = load(transformed)
    return result

if __name__ == "__main__":
    etl_pipeline()
'''


# Singleton instance
_generator_instance: Optional[PipelineGenerator] = None


def get_generator(llm_model: str = "gpt-4", api_key: Optional[str] = None, base_url: Optional[str] = None) -> PipelineGenerator:
    """Get or create pipeline generator instance"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = PipelineGenerator(llm_model, api_key, base_url)
    return _generator_instance
