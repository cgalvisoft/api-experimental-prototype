import json
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.model import Task


@pytest.fixture
def client():
    """Create a test client for the app."""
    return TestClient(app)


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }


def test_create_task(client, sample_task):
    """Test creating a new task."""
    response = client.post("/tasks", json=sample_task)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == sample_task["title"]
    assert data["description"] == sample_task["description"]
    assert data["completed"] == sample_task["completed"]
    assert "id" in data


def test_get_tasks(client, sample_task):
    """Test getting all tasks."""
    # Create a task first
    client.post("/tasks", json=sample_task)
    
    # Get all tasks
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_task(client, sample_task):
    """Test getting a specific task."""
    # Create a task first
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == sample_task["title"]


def test_get_task_not_found(client):
    """Test getting a non-existent task."""
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client, sample_task):
    """Test updating a task."""
    # Create a task first
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {"title": "Updated Task", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == update_data["title"]
    assert data["completed"] == update_data["completed"]
    assert data["description"] == sample_task["description"]  # Should remain unchanged


def test_update_task_not_found(client):
    """Test updating a non-existent task."""
    update_data = {"title": "Updated Task", "completed": True}
    response = client.put("/tasks/9999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(client, sample_task):
    """Test deleting a task."""
    # Create a task first
    create_response = client.post("/tasks", json=sample_task)
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    
    # Verify the task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """Test deleting a non-existent task."""
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_metrics_endpoint(client):
    """Test that the metrics endpoint is available."""
    response = client.get("/metrics")
    assert response.status_code == 200
    # Verificar que la respuesta contiene algún tipo de métrica, sin especificar cuál
    assert "http_request_duration_seconds" in response.text


def test_validation_error(client):
    """Test validation error when creating a task with invalid data."""
    invalid_task = {"title": "", "description": "Missing title"}
    response = client.post("/tasks", json=invalid_task)
    assert response.status_code == 422  # Unprocessable Entity