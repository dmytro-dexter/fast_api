from .service import read_todos, read_todo, create_todo, update_todo, delete_todo
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .deps import get_db
from .schemas import CreateTodoItem, TodoItem, UpdateTodoItem

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/")
def read_todos_route(db: Session = Depends(get_db)) -> list[TodoItem]:
    return read_todos(db)


@router.get("/{todo-id}")
def read_todo_route(todo_id: int, db: Session = Depends(get_db)) -> TodoItem:
    todo = read_todo(todo_id, db)
    return todo


@router.post("/")
def create_todo_route(todo: CreateTodoItem, db: Session = Depends(get_db)) -> TodoItem:
    return create_todo(todo, db)


@router.put("/{todo_id}")
def update_todo_route(todo_id: int, body: UpdateTodoItem, db: Session = Depends(get_db)) -> TodoItem:
    return update_todo(todo_id, body, db)


@router.delete("/{todo_id}")
def delete_todo_route(todo_id: int, db: Session = Depends(get_db)) -> None:
    delete_todo(todo_id, db)
