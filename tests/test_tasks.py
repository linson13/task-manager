"""
Tests for task endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.session import Base, get_db
from app.models.task import TaskStatus, TaskPriority

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Create test client."""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_create_task(client):
    """Test creating a new task."""
    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "priority": "high"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert data["priority"] == "high"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_tasks(client):
    """Test getting all tasks."""
    # Create some tasks
    client.post("/api/v1/tasks", json={"title": "Task 1", "status": "pending"})
    client.post("/api/v1/tasks", json={"title": "Task 2", "status": "in_progress"})
    
    # Get all tasks
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2


def test_get_task_by_id(client):
    """Test getting a specific task."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Specific Task"}
    )
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"


def test_get_nonexistent_task(client):
    """Test getting a task that doesn't exist."""
    response = client.get("/api/v1/tasks/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_task(client):
    """Test updating a task."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Original Title", "status": "pending"}
    )
    task_id = create_response.json()["id"]
    
    # Update the task
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated Title", "status": "completed"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "completed"


def test_update_task_status(client):
    """Test updating only task status."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Task", "status": "pending"}
    )
    task_id = create_response.json()["id"]
    
    # Update status
    response = client.patch(
        f"/api/v1/tasks/{task_id}/status",
        json={"status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_update_task_priority(client):
    """Test updating only task priority."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Task", "priority": "low"}
    )
    task_id = create_response.json()["id"]
    
    # Update priority
    response = client.patch(
        f"/api/v1/tasks/{task_id}/priority",
        json={"priority": "high"}
    )
    assert response.status_code == 200
    assert response.json()["priority"] == "high"


def test_delete_task(client):
    """Test deleting a task."""
    # Create a task
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Task to Delete"}
    )
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 404


def test_filter_tasks_by_status(client):
    """Test filtering tasks by status."""
    # Create tasks with different statuses
    client.post("/api/v1/tasks", json={"title": "Pending Task", "status": "pending"})
    client.post("/api/v1/tasks", json={"title": "Completed Task", "status": "completed"})
    
    # Filter by pending
    response = client.get("/api/v1/tasks?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["status"] == "pending"


def test_filter_tasks_by_priority(client):
    """Test filtering tasks by priority."""
    # Create tasks with different priorities
    client.post("/api/v1/tasks", json={"title": "High Priority", "priority": "high"})
    client.post("/api/v1/tasks", json={"title": "Low Priority", "priority": "low"})
    
    # Filter by high priority
    response = client.get("/api/v1/tasks?priority=high")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["priority"] == "high"


def test_search_tasks(client):
    """Test searching tasks."""
    # Create tasks
    client.post("/api/v1/tasks", json={"title": "Important Meeting", "description": "Discuss project"})
    client.post("/api/v1/tasks", json={"title": "Buy groceries", "description": "Get milk and eggs"})
    
    # Search for "meeting"
    response = client.get("/api/v1/tasks/search?q=meeting")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert "meeting" in data["tasks"][0]["title"].lower()


def test_pagination(client):
    """Test task pagination."""
    # Create 5 tasks
    for i in range(5):
        client.post("/api/v1/tasks", json={"title": f"Task {i}"})
    
    # Get first 2 tasks
    response = client.get("/api/v1/tasks?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 2
    assert data["total"] == 5
    
    # Get next 2 tasks
    response = client.get("/api/v1/tasks?skip=2&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 2


def test_get_statistics(client):
    """Test getting task statistics."""
    # Create tasks with different statuses and priorities
    client.post("/api/v1/tasks", json={"status": "pending", "priority": "high"})
    client.post("/api/v1/tasks", json={"status": "completed", "priority": "low"})
    client.post("/api/v1/tasks", json={"status": "in_progress", "priority": "medium"})
    
    response = client.get("/api/v1/tasks/statistics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_tasks"] == 3
    assert "by_status" in data
    assert "by_priority" in data


def test_validation_error(client):
    """Test validation error handling."""
    # Try to create task without title
    response = client.post("/api/v1/tasks", json={"description": "No title"})
    assert response.status_code == 422


def test_invalid_status(client):
    """Test invalid status value."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Task", "status": "invalid_status"}
    )
    assert response.status_code == 422
