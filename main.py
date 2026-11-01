from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, Task, TaskCreate, TaskRow, engine, get_db

Base.metadata.create_all(engine)  # creates the tasks table if it doesn't exist yet
app = FastAPI(title="Task API")
DB = Annotated[Session, Depends(get_db)]


@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.get("/tasks", response_model=list[Task])
def list_tasks(db: DB):
    return db.scalars(select(TaskRow).order_by(TaskRow.id)).all()


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate, db: DB):
    task = TaskRow(**data.model_dump())
    db.add(task)
    db.commit()
    return task
