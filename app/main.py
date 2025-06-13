import json
import logging
import sys
from typing import Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.model import Task, TaskCreate, TaskUpdate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=json.dumps({
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "message": "%(message)s",
        "module": "%(module)s",
        "function": "%(funcName)s",
        "line": "%(lineno)d"
    }),
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Experimental API",
    description="A simple REST API for managing to-do tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Prometheus metrics
Instrumentator().instrument(app).expose(app)

# In-memory database
tasks_db: Dict[int, Task] = {}
next_id = 1


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate) -> Task:
    """Create a new task."""
    global next_id
    task_id = next_id
    next_id += 1
    
    task_dict = task.model_dump()
    task_dict["id"] = task_id
    new_task = Task(**task_dict)
    tasks_db[task_id] = new_task
    
    logger.info(f"Task created: {task_id}", extra={"task_id": task_id, "endpoint": "/tasks", "method": "POST"})
    return new_task


@app.get("/tasks", response_model=List[Task])
async def get_tasks() -> List[Task]:
    """Get all tasks."""
    logger.info("Retrieved all tasks", extra={"endpoint": "/tasks", "method": "GET"})
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int) -> Task:
    """Get a specific task by ID."""
    if task_id not in tasks_db:
        logger.warning(f"Task not found: {task_id}", extra={"task_id": task_id, "endpoint": f"/tasks/{task_id}", "method": "GET"})
        raise HTTPException(status_code=404, detail="Task not found")
    
    logger.info(f"Retrieved task: {task_id}", extra={"task_id": task_id, "endpoint": f"/tasks/{task_id}", "method": "GET"})
    return tasks_db[task_id]


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task_update: TaskUpdate) -> Task:
    """Update an existing task."""
    if task_id not in tasks_db:
        logger.warning(f"Task not found: {task_id}", extra={"task_id": task_id, "endpoint": f"/tasks/{task_id}", "method": "PUT"})
        raise HTTPException(status_code=404, detail="Task not found")
    
    stored_task = tasks_db[task_id]
    update_data = task_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(stored_task, field, value)
    
    tasks_db[task_id] = stored_task
    logger.info(f"Task updated: {task_id}", extra={"task_id": task_id, "endpoint": f"/tasks/{task_id}", "method": "PUT"})
    return stored_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int) -> None:
    """Delete a task."""
    if task_id not in tasks_db:
        logger.warning(f"Task not found: {task_id}", extra={"task_id": task_id, "endpoint": f"/tasks/{task_id}", "method": "DELETE"})
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    logger.info(f"Task deleted: {task_id}", extra={"task_id": task_id, "endpoint": f"/tasks/{task_id}", "method": "DELETE"})


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}