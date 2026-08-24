"""
Codomax Python Internship - Module 5: Python Application Development
Project: REST API with FastAPI, SQLite Database & Schema Validation
Features:
  - FastAPI web framework with auto-generated Swagger UI docs
  - SQLite database integration with SQL CRUD operations
  - Pydantic models for request/response schema validation
  - API Key Header Authentication
"""

import sqlite3
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

# Database file
DB_NAME = "tasks.db"
API_KEY_NAME = "X-API-KEY"
VALID_API_KEY = "codomax_python_secret_2026"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="Codomax Task Management REST API",
    description="A full-featured REST API built with FastAPI, SQLite, and Pydantic validation.",
    version="1.0.0"
)


# --- DATABASE INITIALIZATION ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'Medium'
        )
    """)
    conn.commit()
    conn.close()

init_db()


# --- PYDANTIC SCHEMAS ---
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, example="Complete Module 5 Assignment")
    description: Optional[str] = Field(None, example="Build a FastAPI backend with SQLite storage")
    status: Optional[str] = Field("pending", example="pending")
    priority: Optional[str] = Field("Medium", example="High")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str


# --- AUTHENTICATION DEPENDENCY ---
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == VALID_API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key. Include 'X-API-KEY: codomax_python_secret_2026' header."
    )


# --- API ENDPOINTS ---

@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Welcome to the Codomax Python REST API",
        "docs_url": "/docs",
        "endpoints": ["/api/tasks (GET, POST)", "/api/tasks/{id} (GET, PUT, DELETE)"]
    }


# 1. Get All Tasks (Public)
@app.get("/api/tasks", response_model=List[TaskResponse], tags=["Tasks"])
def get_all_tasks():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# 2. Get Single Task by ID (Public)
@app.get("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: int):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return dict(row)


# 3. Create Task (Protected by API Key)
@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate, authenticated: str = Security(get_api_key)):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)",
        (task.title, task.description, task.status, task.priority)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority
    }


# 4. Update Task (Protected by API Key)
@app.put("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task: TaskUpdate, authenticated: str = Security(get_api_key)):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    new_title = task.title if task.title is not None else existing["title"]
    new_description = task.description if task.description is not None else existing["description"]
    new_status = task.status if task.status is not None else existing["status"]
    new_priority = task.priority if task.priority is not None else existing["priority"]

    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, status = ?, priority = ? WHERE id = ?",
        (new_title, new_description, new_status, new_priority, task_id)
    )
    conn.commit()
    conn.close()

    return {
        "id": task_id,
        "title": new_title,
        "description": new_description,
        "status": new_status,
        "priority": new_priority
    }


# 5. Delete Task (Protected by API Key)
@app.delete("/api/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, authenticated: str = Security(get_api_key)):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    return {"message": f"Task {task_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_app:app", host="127.0.0.1", port=8000, reload=True)