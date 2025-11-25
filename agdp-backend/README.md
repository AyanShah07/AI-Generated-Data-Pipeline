# AGDP Backend

FastAPI backend for AI-Generated Data Pipelines application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your LLM API key and preferences
```

3. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Endpoints

### Pipelines
- `POST /api/pipelines` - Create new pipeline
- `GET /api/pipelines` - List all pipelines
- `GET /api/pipelines/{id}` - Get pipeline details
- `PUT /api/pipelines/{id}` - Update pipeline
- `DELETE /api/pipelines/{id}` - Delete pipeline
- `POST /api/pipelines/{id}/generate` - Generate code for pipeline

### Executions
- `POST /api/executions` - Start pipeline execution
- `GET /api/executions/{id}` - Get execution details
- `GET /api/pipelines/{id}/executions` - List pipeline executions

### Settings
- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings
