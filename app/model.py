from pydantic import BaseModel, Field
from typing import Optional


class TaskBase(BaseModel):
    """Base model for Task with common fields."""
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    completed: bool = Field(default=False, description="Task completion status")


class TaskCreate(TaskBase):
    """Model for creating a new task."""
    pass


class TaskUpdate(TaskBase):
    """Model for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, min_length=1, description="Task description")
    completed: Optional[bool] = Field(None, description="Task completion status")


class Task(TaskBase):
    """Model for a task with ID."""
    id: int = Field(..., description="Task unique identifier")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Complete project",
                "description": "Finish the REST API demo project",
                "completed": False
            }
        }
    }