from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from uuid import UUID
from models import Task, TaskCreate
from task_service import task_service

app = FastAPI(title="Task Manager")

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return task_service.get_all_tasks()


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    return task_service.create_task(task)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: UUID):
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_service.delete_task(task_id)
    return {"message": "Task deleted"}