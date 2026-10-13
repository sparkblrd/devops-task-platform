# DevOps Task Platform

A small REST API built with **FastAPI**. This is **Milestone 1** of a hands-on DevOps portfolio project. The next milestones will add PostgreSQL, Docker, CI/CD, Kubernetes and observability.

> **Current limitation:** Tasks are stored **only in process memory**. They disappear after an application restart and are **not shared** across multiple Uvicorn workers or Kubernetes replicas. This release is a learning-stage application, **not a production-ready service**.

## Stack

- Python 3.12+
- FastAPI, Pydantic v2, Uvicorn
- pytest, FastAPI TestClient (HTTPX)

## Quick start (Linux / WSL / macOS)

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1` (create it with `py -m venv .venv`).

Open:

- API documentation: http://127.0.0.1:8000/docs
- API root: http://127.0.0.1:8000/
- Liveness endpoint: http://127.0.0.1:8000/health

`--reload` is **only for local development**, not deployment.

## API

| Method | Endpoint | Behavior |
|---|---|---|
| `GET` | `/` | Service information (`200`) |
| `GET` | `/health` | Liveness check (`200`) |
| `GET` | `/api/v1/tasks` | List tasks (`200`) |
| `POST` | `/api/v1/tasks` | Create a task (`201`) |
| `GET` | `/api/v1/tasks/{task_id}` | Read a task (`200` or `404`) |
| `DELETE` | `/api/v1/tasks/{task_id}` | Delete a task (`204` or `404`) |

Invalid inputs return `422 Unprocessable Entity`.

Task creation example:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Deploy the API","description":"Kubernetes later","completed":false}'
```

Expected response (`201`):

```json
{
  "id": 1,
  "title": "Deploy the API",
  "description": "Kubernetes later",
  "completed": false
}
```

Get all tasks:

```bash
curl http://127.0.0.1:8000/api/v1/tasks
```

Delete task ID 1:

```bash
curl -i -X DELETE http://127.0.0.1:8000/api/v1/tasks/1
```

## Tests

```bash
python -m pytest -v
```

Tests replace the application's storage dependency with a new in-memory store **for each test**. No PostgreSQL, Docker, or external services are necessary yet.

## Project structure

```text
devops-task-platform/
├── app/
│   ├── __init__.py
│   ├── main.py                # Creates FastAPI app and system routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py            # Request and response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py           # API endpoints
│   └── services/
│       ├── __init__.py
│       └── task_service.py    # In-memory task storage
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Roadmap

- [x] Milestone 1: FastAPI REST API, validation, unit/API tests
- [ ] Milestone 2: PostgreSQL and persistence
- [ ] Milestone 3: Docker & Docker Compose
- [ ] Milestone 4: GitHub Actions & GHCR
- [ ] Milestone 5: Kubernetes & Ingress
- [ ] Milestone 6: Helm
- [ ] Milestone 7: Prometheus, Grafana, Loki & alerts
- [ ] Milestone 8: VPS deployment, TLS, backups, rollbacks and portfolio documentation

### Kubernetes design question

When a user creates a task on replica A and reads it from replica B, they might **not** see the task: each worker holds separate memory. A persistent shared data store (PostgreSQL) will address this problem in the following milestone.
