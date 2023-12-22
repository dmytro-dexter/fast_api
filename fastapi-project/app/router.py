import fastapi
from typing import List
from .models import todos_db
from .schemas import Todo
from .constants import error
from .service import get_todo_by_id

router = fastapi.APIRouter()


@router.post("/todos/")
def create_todo(todo: Todo):
    """
        Create a new to-do item.

        Parameters:
        - todo: The data for the new to-do item.

        Returns:
        - Todo: The newly created to-do item.
    """
    todos_db.append(todo)
    return todo


@router.get("/todos/", response_model=List[Todo])
def read_todos():
    """
        Get a list of all to-do items.

        Returns:
        - List[Todo]: List of all to-do items.
    """
    return todos_db


@router.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    """
        Get information about a specific to-do item.

        Parameters:
        - todo_id: The ID of the to-do item.

        Returns:
        - Todo: Information about the to-do item.

        Raises:
        - HTTPException 404: If the to-do item with the specified ID is not found.
    """
    todo = get_todo_by_id(todo_id)
    if todo is None:
        raise error
    return todo


@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, completed: bool):
    """
        Update the completion status of a to-do item.

        Parameters:
        - todo_id: The ID of the to-do item to be updated.
        - completed: The new completion status.

        Returns:
        - Todo: The updated to-do item.

        Raises:
        - HTTPException 404: If the to-do item with the specified ID is not found.
    """
    todo = get_todo_by_id(todo_id)
    if todo is None:
        raise error
    todo.completed = completed
    return todo


@router.delete("/todos/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    """
        Delete a to-do item.

        Parameters:
        - todo_id: The ID of the to-do item to be deleted.

        Returns:
        - Todo: The deleted to-do item.

        Raises:
        - HTTPException 404: If the to-do item with the specified ID is not found.
    """
    todo = get_todo_by_id(todo_id)
    if todo is None:
        raise error
    todos_db.remove(todo)
    return todo
