# Task API

A simple REST API for managing tasks, built with FastAPI and SQLAlchemy.

This is the code from my YouTube video on building a CRUD API with FastAPI.

## Setup

Needs Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
fastapi dev
```

Open http://localhost:8000/docs to try the API.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/tasks` | List tasks (`skip`, `limit` for paging) |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create a task |
| PATCH | `/tasks/{id}` | Update a task (send only the fields you want to change) |
| DELETE | `/tasks/{id}` | Delete a task |

Tasks are stored in a local SQLite file, `tasks.db`, created on first run.
