# OES — Your Personal AI Memory Engine

OES is a local-first AI application that preserves and connects learning notes,
project decisions, experiments, errors, and solutions.

## Current features

- FastAPI backend
- Root and health-check endpoints
- Interactive API documentation
- Automated endpoint tests

## Setup

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r backend/requirements.txt
```

## Run the backend

From the project root:

```powershell
python -m uvicorn app.main:app --app-dir backend --reload
```

Open http://127.0.0.1:8000/docs for API documentation.

## Run tests

```powershell
python -m pytest backend/tests -v
```

## Project status

Day 1: Backend foundation and initial tests.
