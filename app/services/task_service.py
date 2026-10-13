
from typing import Iterator

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.task import TaskCreate, TaskResponse
from app.models.task_orm import Task


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def list_tasks(self) -> list[TaskResponse]:
        tasks = self.db.scalars(
            select(Task).order_by(Task.id)
        ).all()

        return [
            TaskResponse.model_validate(task, from_attributes=True)
            for task in tasks
        ]

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        task = Task(**payload.model_dump())

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return TaskResponse.model_validate(
            task, from_attributes=True
        )

    def get_task(self, task_id: int) -> TaskResponse | None:
        task = self.db.get(Task, task_id)

        if task is None:
            return None

        return TaskResponse.model_validate(
            task, from_attributes=True
        )

    def delete_task(self, task_id: int) -> bool:
        task = self.db.get(Task, task_id)

        if task is None:
            return False

        self.db.delete(task)
        self.db.commit()
        return True


def get_task_service() -> Iterator[TaskService]:
    with SessionLocal() as session:
        yield TaskService(session)

