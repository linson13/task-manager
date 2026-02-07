"""
Task database model.
Defines the Task table structure using SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Text, Enum, Date, DateTime
from sqlalchemy.sql import func
import enum
from app.database.session import Base


class TaskStatus(str, enum.Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, enum.Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    """
    Task model representing a task in the database.
    
    Attributes:
        id: Unique identifier
        title: Task title (required)
        description: Detailed description (optional)
        status: Current status (pending, in_progress, completed)
        priority: Priority level (low, medium, high)
        due_date: Optional due date
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """
    
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False,
        index=True
    )
    priority = Column(
        Enum(TaskPriority),
        default=TaskPriority.MEDIUM,
        nullable=False,
        index=True
    )
    due_date = Column(Date, nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status.value})>"
