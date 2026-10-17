# OES — Your Personal AI Memory Engine

OES (Your Personal AI Memory Engine) is a local-first application designed to preserve and organize your learning journey, project experiences, technical decisions, bugs, and solutions.

The long-term goal is to build a personal memory system that can connect past experiences and help retrieve relevant knowledge as your learning progresses.

## Current Features

- FastAPI backend with organized API routes
- Environment-based configuration using Pydantic Settings
- Root and health-check endpoints
- SQLite database for persistent memory storage
- UUID-based memory identifiers
- UTC ISO 8601 timestamps
- Memory creation, retrieval, and listing APIs
- Input validation for memory content and types
- Deterministic newest-first memory ordering
- Pydantic request and response schemas
- Configurable application logging
- Automated tests using pytest and FastAPI TestClient
- Interactive Swagger/OpenAPI documentation

## Technology Stack

- Python 3.14
- FastAPI
- Pydantic and Pydantic Settings
- SQLite using Python's built-in `sqlite3` module
- Uvicorn
- pytest
- Git

## Setup

From the project root, create and activate a virtual environment:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r backend\requirements.txt
```

## Configuration

Create a local environment file if you need to override the defaults:

```powershell
Copy-Item .env.example .env
```

Available settings:

| Environment Variable | Default                           |
| -------------------- | --------------------------------- |
| `OES_APP_NAME`       | `OES - Personal AI Memory Engine` |
| `OES_APP_VERSION`    | `0.1.0`                           |
| `OES_ENV`            | `development`                     |
| `OES_LOG_LEVEL`      | `INFO`                            |
| `OES_API_PREFIX`     | `/api/v1`                         |
| `OES_DATABASE_PATH`  | `data/oes.db`                     |

The application reads `.env` from the current working directory and supports environment-variable overrides.

The SQLite database is created automatically when the application starts. The default location is `data/oes.db`. Local database files and `.env` are excluded from Git.

## Run the Backend

From the project root:

```powershell
python -m uvicorn app.main:app --app-dir backend --reload
```

Open the API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json
- Health check: http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint                       | Purpose                 | Success Status |
| ------ | ------------------------------ | ----------------------- | -------------- |
| GET    | `/`                            | Welcome response        | `200 OK`       |
| GET    | `/health`                      | Backend health status   | `200 OK`       |
| POST   | `/api/v1/memories`             | Create a memory         | `201 Created`  |
| GET    | `/api/v1/memories`             | List all memories       | `200 OK`       |
| GET    | `/api/v1/memories/{memory_id}` | Retrieve a memory by ID | `200 OK`       |

An unknown memory ID returns `404 Not Found`. Invalid memory request payloads return `422 Unprocessable Entity`.

### Memory Data Model

Each memory contains:

| Field         | Description                                        |
| ------------- | -------------------------------------------------- |
| `id`          | UUID stored as text                                |
| `content`     | Non-empty text, maximum 10,000 characters          |
| `memory_type` | `learning`, `project`, `decision`, `bug`, or `fix` |
| `created_at`  | UTC creation timestamp in ISO 8601 format          |
| `updated_at`  | UTC update timestamp in ISO 8601 format            |

Memories are listed newest first, ordered by `created_at` descending and then `id` descending to break timestamp ties deterministically.

### Create a Memory

Example request body for `POST /api/v1/memories`:

```json
{
  "content": "Learned how gradient descent updates model parameters.",
  "memory_type": "learning"
}
```

The response contains the saved memory, including its generated UUID and timestamps.

### List Memories

Send a GET request to `/api/v1/memories`.

The response includes a `memories` array and a `count` field.

### Retrieve a Memory

Send a GET request to `/api/v1/memories/{memory_id}`, replacing `memory_id` with the UUID returned when the memory was created.

## Run Tests

Run the complete test suite:

```powershell
python -m pytest backend\tests -v
```

Tests cover:

- Configuration defaults and environment overrides
- SQLite table creation and database constraints
- Persistent storage
- Memory service operations
- API success and error responses
- Request validation
- Memory ordering
- OpenAPI documentation
- Root, health, and unknown endpoints

API tests use temporary databases to avoid modifying the development database.

## Project Structure

```text
backend/
  app/
    api/
      routes/
        health.py
        memories.py
    core/
      config.py
      database.py
      logging_config.py
    models/
      schemas.py
    services/
      memory_service.py
    main.py
  tests/
    test_config.py
    test_database.py
    test_health.py
    test_memories_api.py
    test_memory_service.py
data/
  .gitkeep
docs/
  decisions/
experiments/
```

## Development Status

- **Day 1:** Initial backend, project structure, root and health endpoints, and tests.
- **Day 2:** Configuration, API organization, response schemas, logging, and expanded tests.
- **Day 3:** SQLite persistence, memory service, memory API endpoints, request validation, persistence verification, and automated tests.

## Planned Future Work

Future phases may introduce memory search, retrieval-augmented generation (RAG), knowledge graphs, and LLM-powered explanations. These are planned capabilities and are not part of the current implementation.
