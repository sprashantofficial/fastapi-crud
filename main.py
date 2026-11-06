import logging
import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from database import Base, Task, TaskCreate, TaskRow, TaskUpdate, engine, get_db

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("tasks")

Base.metadata.create_all(engine)  # creates the tasks table if it doesn't exist yet
app = FastAPI(title="Task API")
DB = Annotated[Session, Depends(get_db)]


def find_task(db: Session, task_id: int) -> TaskRow:
    task = db.get(TaskRow, task_id)
    if task is None:
        raise HTTPException(404, f"Task {task_id} not found")
    return task


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(Path(__file__).parent / "index.html")


@app.get("/health")
def health(db: DB):
    db.execute(text("SELECT 1"))  # fails if the database can't be reached
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task])
def list_tasks(db: DB, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)):
    return db.scalars(select(TaskRow).order_by(TaskRow.id).offset(skip).limit(limit)).all()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, db: DB):
    return find_task(db, task_id)


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate, db: DB):
    task = TaskRow(**data.model_dump())
    db.add(task)
    db.commit()
    log.info("Created task %s", task.id)
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskUpdate, db: DB):
    task = find_task(db, task_id)
    for field, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(task, field, value)
    db.commit()
    log.info("Updated task %s", task_id)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: DB):
    db.delete(find_task(db, task_id))
    db.commit()
    log.info("Deleted task %s", task_id)
