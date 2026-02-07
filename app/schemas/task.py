"""
Pydantic schemas for request validation and response serialization.
Defines the structure of API inputs and outputs.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base schema with common task fields."""
    
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, description="Detailed description of the task")
    status: Optional[TaskStatus] = Field(TaskStatus.PENDING, description="Current status")
    priority: Optional[TaskPriority] = Field(TaskPriority.MEDIUM, description="Priority level")
    due_date: Optional[date] = Field(None, description="Due date for the task")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None


class TaskStatusUpdate(BaseModel):
    """Schema for updating only task status."""
    status: TaskStatus = Field(..., description="New status")


class TaskPriorityUpdate(BaseModel):
    """Schema for updating only task priority."""
    priority: TaskPriority = Field(..., description="New priority")


class TaskResponse(TaskBase):
    """Schema for task response with database fields."""
    
    id: int = Field(..., description="Unique task identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""
    
    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    skip: int = Field(..., description="Number of tasks skipped")
    limit: int = Field(..., description="Maximum tasks returned")


class HealthResponse(BaseModel):
    """Schema for health check response."""
    
    status: str = Field(..., description="API status")
    timestamp: datetime = Field(..., description="Current timestamp")


class DetailedHealthResponse(HealthResponse):
    """Schema for detailed health check with database status."""
    
    database: str = Field(..., description="Database connection status")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")


class MessageResponse(BaseModel):
    """Schema for simple message responses."""
    
    message: str = Field(..., description="Response message")
