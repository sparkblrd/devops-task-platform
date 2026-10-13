"""Temporary in-memory storage for tasks.

NOTE: Data is lost at process restart and is NOT shared between worker processes
or Kubernetes replicas. A PostgreSQL-backed repository will replace this later.
"""

from functools import lru_cache
from threading import Lock

from app.models.task import TaskCreate, TaskResponse


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[int, TaskResponse] = {}
        self._next_id = 1
        self._lock = Lock()

    def list_tasks(self) -> list[TaskResponse]:
        with self._lock:
            return list(self._tasks.values())

    def create_task(self, payload: TaskCreate) -> TaskResponse:
        with self._lock:
            task = TaskResponse(id=self._next_id, **payload.model_dump())
            self._tasks[task.id] = task
            self._next_id += 1
            return task

    def get_task(self, task_id: int) -> TaskResponse | None:
        with self._lock:
            return self._tasks.get(task_id)

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None


@lru_cache(maxsize=1)
def get_task_service() -> TaskService:
    """Use a shared service instance within this Python worker process."""
    return TaskService()
