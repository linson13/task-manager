"""
Custom exceptions for the Task Management API.
"""

from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    """Exception raised when a task is not found."""
    
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


class TaskValidationException(HTTPException):
    """Exception raised when task validation fails."""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class DatabaseException(HTTPException):
    """Exception raised when database operation fails."""
    
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
