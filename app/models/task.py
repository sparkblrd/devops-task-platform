"""Pydantic schemas used by the tasks API."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    """Request data needed to create a task."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    completed: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, title: str) -> str:
        """Trim whitespace and reject titles that contain only whitespace."""
        title = title.strip()
        if not title:
            raise ValueError("title must not be blank")
        return title


class TaskResponse(TaskCreate):
    """Task returned by the REST API."""

    id: int = Field(gt=0)
