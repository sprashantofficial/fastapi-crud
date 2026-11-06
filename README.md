# Task API

A to-do app with a REST API, built with FastAPI and SQLAlchemy. It has a simple web page for managing tasks, and the same API can be used directly from `/docs` or curl.

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
fastapi dev      # development, auto-reload
fastapi run      # production
```

Open http://localhost:8000 for the to-do app, or http://localhost:8000/docs for the API docs.

## Use the app

The page at http://localhost:8000 is a simple to-do list that runs on this API:

- Type a task and press Enter (or click **Add**).
- Tick the checkbox to mark a task done. Untick it to undo.
- Click **Edit** to rename a task.
- Click **Delete** to remove it.

Everything you do here goes through the same endpoints listed below, and is saved in the database.

## Try the API

The `/docs` page lists every endpoint. To call one, click it to expand it, click **Try it out**, fill in the fields, then click **Execute**. The response shows up just below.

Go through them in this order:

1. **Create a task.** Open `POST /tasks` and use this body:
   ```json
   {
     "title": "Learn FastAPI"
   }
   ```
   You should get `201` and the new task. Note its `id`; the next steps use it. Create one or two more with different titles.

2. **List tasks.** Open `GET /tasks` and execute it. You should get `200` and all the tasks you created.

3. **Get one task.** Open `GET /tasks/{task_id}`, enter the `id` from step 1 as the `task_id`, and execute. You should get `200` and just that task.

4. **Update a task.** Open `PATCH /tasks/{task_id}`, enter the same `id`, and use this body:
   ```json
   {
     "completed": true
   }
   ```
   You should get `200`. `completed` is now `true` and the title is unchanged.

5. **Delete a task.** Open `DELETE /tasks/{task_id}`, enter the same `id`, and execute. You should get `204` with an empty body.

6. **Check the errors.**
   - Run `GET /tasks/{task_id}` with that `id` again. You should get `404`, because the task is gone.
   - Run `POST /tasks` with `{}` as the body. You should get `422`, because `title` is required.

Each create, update and delete also prints a log line in the terminal running the server, and the change shows up in the to-do page when you refresh it.

### From the terminal

If you'd rather use curl, open a second terminal while the server is running. Replace `1` with the `id` the first command returns:

```bash
curl -X POST localhost:8000/tasks -H "Content-Type: application/json" -d '{"title": "Learn FastAPI"}'
curl localhost:8000/tasks
curl localhost:8000/tasks/1
curl -X PATCH localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"completed": true}'
curl -X DELETE localhost:8000/tasks/1 -i
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | The to-do page |
| GET | `/health` | Health check (also checks the database) |
| GET | `/tasks` | List tasks (`skip`, `limit` for paging) |
| GET | `/tasks/{id}` | Get one task |
| POST | `/tasks` | Create a task |
| PATCH | `/tasks/{id}` | Update a task (send only the fields you want to change) |
| DELETE | `/tasks/{id}` | Delete a task |

## Database

By default the app uses SQLite, a database that keeps everything in a single file. It comes built into Python, so there's nothing to install. The first time the app starts, it creates that file, `tasks.db`, in the project folder. Your tasks live there, so they're still there after a restart. To start over with an empty list, stop the server and delete `tasks.db`.

SQLAlchemy is the library the code uses to talk to the database. The same code works with SQLite or PostgreSQL; only `DATABASE_URL` changes.

For production, use PostgreSQL. Install its driver (SQLite's comes with Python, PostgreSQL's doesn't), create an empty database, then set `DATABASE_URL` before starting the app:

```bash
pip install "psycopg[binary]"
export DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/tasks"
fastapi run
```

The `tasks` table is created automatically on startup.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./tasks.db` | Where tasks are stored |
| `LOG_LEVEL` | `INFO` | How much the app logs |

## Files

- `main.py`: the endpoints, and the route that serves the to-do page
- `database.py`: the database connection, the `tasks` table, and the request/response models
- `index.html`: the to-do page, styled with [Bootstrap](https://getbootstrap.com) (loaded from a CDN, so the page needs an internet connection)
