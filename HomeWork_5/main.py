from random import choice
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int = Field(default=None)
    title: str = Field(min_length=2, max_length=50)
    description: str = Field(max_length=200)
    status: str

tasks = []

for i in range(1, 21):
    task = Task(id=i,
                title=f'Title{i}',
                description='Some description',
                status=f'{choice(["todo", "in progress", "done"])}')
    tasks.append(task)

@app.get('/')
def home():
    return{'messsage': 'Home Work 5'}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    if id >= len(tasks) or id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[id]

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks.append(task)
    return task

@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, updated_task: Task):
    if id >= len(tasks) or id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[id] = updated_task
    return updated_task

@app.delete("/tasks/{id}", response_model=Task)
def delete_task(id: int):
    if id >= len(tasks) or id < 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks.pop(id)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)