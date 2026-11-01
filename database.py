from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine, expire_on_commit=False)


def get_db():
    """Gives each request its own database session and closes it afterwards."""
    with SessionLocal() as db:
        yield db


# The "tasks" table in the database
class Base(DeclarativeBase):
    pass


class TaskRow(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


# What the API accepts and returns
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool = False


class Task(TaskCreate):
    model_config = ConfigDict(from_attributes=True)  # can be built from a TaskRow
    id: int
    created_at: datetime
