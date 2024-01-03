from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from .deps import get_db
from .schemas import TodoItem, CreateTodoItem, UpdateTodoItem
from .models import TodoItemDB


def find_todo_object(todo_id: int, db: Session = Depends(get_db)):
    todo_object = db.query(TodoItemDB).filter(TodoItemDB.id == todo_id).first()
    if todo_object is None:
        raise HTTPException(status_code=404, detail=f"ID {todo_id}: Does not exist")
    return todo_object


def read_todos(db: Session) -> list[TodoItem]:
    todo_items = db.query(TodoItemDB).all()
    return [TodoItem(**item.__dict__) for item in todo_items]


def read_todo(todo_id: int, db: Session = Depends(get_db)) -> TodoItem:
    return TodoItem(**find_todo_object(todo_id, db).__dict__)


def create_todo(todo: CreateTodoItem, db: Session = Depends(get_db)) -> TodoItem:
    todo_model = TodoItemDB(
        title=todo.title,
        description=todo.description,
        done=todo.done
    )

    db.add(todo_model)
    db.commit()
    return todo_model


def update_todo(todo_id: int, body: UpdateTodoItem, db: Session = Depends(get_db)) -> TodoItem:
    todo_object = find_todo_object(todo_id, db)

    if todo_object:
        for key, value in UpdateTodoItem(**body.__dict__):
            setattr(todo_object, key, value)
    db.commit()
    db.refresh(todo_object)
    return TodoItem(**todo_object.__dict__)


def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> None:
    todo_model = find_todo_object(todo_id, db)

    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"ID {todo_id} does not exist")
    db.query(TodoItemDB).filter(TodoItemDB.id == todo_id).delete()
    db.commit()
