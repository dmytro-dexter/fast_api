from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


todos_db = []


def get_todo_by_id(todo_id: int):
    for element in todos_db:
        if element.id == todo_id:
            return element
    return None


@app.post("/todos/")
def create_todo(todo: Todo):
    todos_db.append(todo)
    return todo


@app.get("/todos/", response_model=List[Todo])
def read_todos():
    return todos_db


@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    todo = get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, completed: bool):
    todo = get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = completed
    return todo


@app.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    todo = get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos_db.remove(todo)
    return todo
