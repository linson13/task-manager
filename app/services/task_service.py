"""
Task service module.
Contains business logic for task operations.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate
from app.utils.exceptions import TaskNotFoundException, TaskValidationException


class TaskService:
    """Service class for task-related operations."""
    
    @staticmethod
    def create_task(db: Session, task_data: TaskCreate) -> Task:
        """
        Create a new task.
        
        Args:
            db: Database session
            task_data: Task creation data
            
        Returns:
            Created task
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            due_date=task_data.due_date
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def get_task(db: Session, task_id: int) -> Task:
        """
        Get a task by ID.
        
        Args:
            db: Database session
            task_id: Task ID
            
        Returns:
            Task object
            
        Raises:
            TaskNotFoundException: If task not found
        """
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise TaskNotFoundException(task_id)
        
        return task
    
    @staticmethod
    def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> tuple[List[Task], int]:
        """
        Get list of tasks with optional filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum records to return
            status: Filter by status
            priority: Filter by priority
            
        Returns:
            Tuple of (tasks list, total count)
        """
        query = db.query(Task)
        
        # Apply filters
        if status:
            query = query.filter(Task.status == status)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
        
        return tasks, total
    
    @staticmethod
    def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
        """
        Update a task.
        
        Args:
            db: Database session
            task_id: Task ID
            task_data: Update data
            
        Returns:
            Updated task
            
        Raises:
            TaskNotFoundException: If task not found
        """
        task = TaskService.get_task(db, task_id)
        
        # Update only provided fields
        update_data = task_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(task, field, value)
        
        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def update_task_status(db: Session, task_id: int, status: TaskStatus) -> Task:
        """
        Update task status.
        
        Args:
            db: Database session
            task_id: Task ID
            status: New status
            
        Returns:
            Updated task
        """
        task = TaskService.get_task(db, task_id)
        task.status = status
        
        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def update_task_priority(db: Session, task_id: int, priority: TaskPriority) -> Task:
        """
        Update task priority.
        
        Args:
            db: Database session
            task_id: Task ID
            priority: New priority
            
        Returns:
            Updated task
        """
        task = TaskService.get_task(db, task_id)
        task.priority = priority
        
        db.commit()
        db.refresh(task)
        
        return task
    
    @staticmethod
    def delete_task(db: Session, task_id: int) -> None:
        """
        Delete a task.
        
        Args:
            db: Database session
            task_id: Task ID
            
        Raises:
            TaskNotFoundException: If task not found
        """
        task = TaskService.get_task(db, task_id)
        
        db.delete(task)
        db.commit()
    
    @staticmethod
    def search_tasks(
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Task], int]:
        """
        Search tasks by title or description.
        
        Args:
            db: Database session
            query: Search query
            skip: Number of records to skip
            limit: Maximum records to return
            
        Returns:
            Tuple of (tasks list, total count)
        """
        search_filter = (
            Task.title.ilike(f"%{query}%") |
            Task.description.ilike(f"%{query}%")
        )
        
        query_obj = db.query(Task).filter(search_filter)
        total = query_obj.count()
        
        tasks = query_obj.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
        
        return tasks, total
    
    @staticmethod
    def get_task_statistics(db: Session) -> dict:
        """
        Get task statistics.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with statistics
        """
        total_tasks = db.query(Task).count()
        pending = db.query(Task).filter(Task.status == TaskStatus.PENDING).count()
        in_progress = db.query(Task).filter(Task.status == TaskStatus.IN_PROGRESS).count()
        completed = db.query(Task).filter(Task.status == TaskStatus.COMPLETED).count()
        
        high_priority = db.query(Task).filter(Task.priority == TaskPriority.HIGH).count()
        medium_priority = db.query(Task).filter(Task.priority == TaskPriority.MEDIUM).count()
        low_priority = db.query(Task).filter(Task.priority == TaskPriority.LOW).count()
        
        return {
            "total_tasks": total_tasks,
            "by_status": {
                "pending": pending,
                "in_progress": in_progress,
                "completed": completed
            },
            "by_priority": {
                "high": high_priority,
                "medium": medium_priority,
                "low": low_priority
            }
        }
