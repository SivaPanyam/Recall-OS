# OES — Your Personal AI Memory Engine

OES is a local-first AI application designed to preserve and connect learning notes, project decisions, experiments, errors, and solutions.

## Current Features

- FastAPI backend
- Environment-based configuration using Pydantic Settings
- Root and health-check endpoints
- Separate health router
- Pydantic response schemas
- Configurable application logging
- Automated tests using pytest and FastAPI TestClient
- Interactive Swagger/OpenAPI documentation

## Requirements

- Python 3.14
- PowerShell on Windows
- Git

## Setup

From the project root, create and activate the virtual environment:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r backend\requirements.txt
```

## Configuration

Copy the example configuration if you need local overrides:

```powershell
Copy-Item .env.example .env
```

Available settings:

| Variable          | Default                           |
| ----------------- | --------------------------------- |
| `OES_APP_NAME`    | `OES - Personal AI Memory Engine` |
| `OES_APP_VERSION` | `0.1.0`                           |
| `OES_ENV`         | `development`                     |
| `OES_LOG_LEVEL`   | `INFO`                            |
| `OES_API_PREFIX`  | `/api/v1`                         |

The application reads `.env` from the current working directory and supports environment-variable overrides. Keep secrets out of Git and logs.

## Run the Backend

From the project root:

```powershell
python -m uvicorn app.main:app --app-dir backend --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint  | Purpose               |
| ------ | --------- | --------------------- |
| GET    | `/`       | Welcome response      |
| GET    | `/health` | Backend health status |

The `/api/v1` prefix is reserved in configuration for future versioned APIs. It is not applied to the current root or health endpoints.

## Run Tests

```powershell
python -m pytest backend\tests -v
```

Tests cover configuration, logging validation, endpoint responses, response schemas, OpenAPI documentation, and unknown routes.

## Project Structure

```text
backend/
  app/
    api/routes/     # API route definitions
    core/           # Configuration and logging
    models/         # Response schemas
    services/       # Business logic added as needed
    main.py         # Application setup
  tests/             # Automated tests
data/                # Local application data
docs/decisions/      # Architecture decision records
experiments/         # AI engineering experiments
```

## Development Status

- Day 1: Initial backend, project structure, and endpoint tests.
- Day 2: Configuration, API organization, response schemas, logging, and expanded tests.
- Next: Persistent memory storage and its API design.
