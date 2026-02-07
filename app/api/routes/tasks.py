"""
Task API routes.
Defines all task-related endpoints.
"""

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.schemas.task import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    TaskStatusUpdate, TaskPriorityUpdate, MessageResponse
)
from app.services.task_service import TaskService
from app.models.task import TaskStatus, TaskPriority
from app.config import settings

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with title, description, priority, status, and due date"
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Create a new task.
    
    - **title**: Task title (required, max 200 characters)
    - **description**: Detailed description (optional)
    - **status**: pending, in_progress, or completed (default: pending)
    - **priority**: low, medium, or high (default: medium)
    - **due_date**: Due date in YYYY-MM-DD format (optional)
    """
    created_task = TaskService.create_task(db, task)
    return created_task


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Get all tasks",
    description="Retrieve a list of tasks with optional filtering and pagination"
)
def get_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(
        settings.default_page_size,
        ge=1,
        le=settings.max_page_size,
        description="Maximum number of tasks to return"
    ),
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    Get all tasks with optional filtering.
    
    - **skip**: Number of tasks to skip (for pagination)
    - **limit**: Maximum tasks to return (default: 100, max: 1000)
    - **status**: Filter by status (pending, in_progress, completed)
    - **priority**: Filter by priority (low, medium, high)
    """
    tasks, total = TaskService.get_tasks(db, skip, limit, status, priority)
    
    return TaskListResponse(
        tasks=tasks,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/search",
    response_model=TaskListResponse,
    summary="Search tasks",
    description="Search tasks by title or description"
)
def search_tasks(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0),
    limit: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    Search tasks by title or description.
    
    - **q**: Search query (searches in title and description)
    - **skip**: Number of tasks to skip
    - **limit**: Maximum tasks to return
    """
    tasks, total = TaskService.search_tasks(db, q, skip, limit)
    
    return TaskListResponse(
        tasks=tasks,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get(
    "/statistics",
    summary="Get task statistics",
    description="Get statistics about tasks (counts by status and priority)"
)
def get_task_statistics(
    db: Session = Depends(get_db)
) -> dict:
    """
    Get task statistics including counts by status and priority.
    """
    return TaskService.get_task_statistics(db)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID"
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Get a specific task by ID.
    
    - **task_id**: Unique task identifier
    """
    task = TaskService.get_task(db, task_id)
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    description="Update a task (all fields)"
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update a task completely.
    
    - **task_id**: Task to update
    - Provide any fields you want to update
    """
    updated_task = TaskService.update_task(db, task_id, task_update)
    return updated_task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Partially update task",
    description="Update specific fields of a task"
)
def partial_update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Partially update a task.
    
    - **task_id**: Task to update
    - Only provide the fields you want to change
    """
    updated_task = TaskService.update_task(db, task_id, task_update)
    return updated_task


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="Update task status",
    description="Update only the status of a task"
)
def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update task status only.
    
    - **task_id**: Task to update
    - **status**: New status (pending, in_progress, completed)
    """
    updated_task = TaskService.update_task_status(db, task_id, status_update.status)
    return updated_task


@router.patch(
    "/{task_id}/priority",
    response_model=TaskResponse,
    summary="Update task priority",
    description="Update only the priority of a task"
)
def update_task_priority(
    task_id: int,
    priority_update: TaskPriorityUpdate,
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update task priority only.
    
    - **task_id**: Task to update
    - **priority**: New priority (low, medium, high)
    """
    updated_task = TaskService.update_task_priority(db, task_id, priority_update.priority)
    return updated_task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task permanently"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a task permanently.
    
    - **task_id**: Task to delete
    """
    TaskService.delete_task(db, task_id)
    return None
