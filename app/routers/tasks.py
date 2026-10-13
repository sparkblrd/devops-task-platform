"""HTTP routes for task management."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status

from app.models.task import TaskCreate, TaskResponse
from app.services.task_service import TaskService, get_task_service

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
TaskId = Annotated[int, Path(gt=0, description="Positive task identifier")]


@router.get("", response_model=list[TaskResponse])
def list_tasks(service: TaskServiceDep) -> list[TaskResponse]:
    return service.list_tasks()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, service: TaskServiceDep) -> TaskResponse:
    return service.create_task(payload)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: TaskId, service: TaskServiceDep) -> TaskResponse:
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: TaskId, service: TaskServiceDep) -> Response:
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
