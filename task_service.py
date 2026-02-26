import json
from uuid import uuid4, UUID
from typing import List
from pathlib import Path
from models import Task, TaskCreate


DATA_FILE = Path("data/tasks.json")

class TaskService:
    def __init__(self):
        self.tasks: List[Task] = []
        self._ensure_file()
        self.load_tasks()

    def _ensure_file(self):
        if not DATA_FILE.exists():
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    def load_tasks(self):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            self.tasks = [Task(**task) for task in data]

    def save_tasks(self):
        with open(DATA_FILE, "w") as f:
            json.dump(
                [task.model_dump() for task in self.tasks],
                f,
                indent=4,
                default=str
            )

    def create_task(self, task_data: TaskCreate) -> Task:
        task = Task(id=uuid4(), **task_data.model_dump())
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

    def get_task(self, task_id: UUID):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def delete_task(self, task_id: UUID):
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()


task_service = TaskService()