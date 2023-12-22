import fastapi
from .service import *

from .schemas import Todo

router = fastapi.APIRouter()


@router.post("/todos/")
def create_todo_route(todo: Todo):
    return create_todo(todo)


@router.get("/todos/", response_model=dict)
def read_todos_route():
    return read_todos()


@router.get("/todos/{todo_id}", response_model=Todo)
def read_todo_route(todo_id: int):
    return read_todo(todo_id)


@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo_route(todo_id: int, completed: bool):
    return update_todo(todo_id, completed)


@router.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo_route(todo_id: int):
    return delete_todo(todo_id)
