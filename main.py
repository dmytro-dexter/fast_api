from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Todo(BaseModel):
    """
       Attributes:
       - id: Unique identifier for the to-do item.
       - title: Title of the to-do item.
       - description: Description of the item.
       - completed: Indicates whether the to-do item is completed or not.
    """
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
    """
        Create a new to-do item.

        Parameters:
        - todo: The data for the new to-do item.

        Returns:
        - Todo: The newly created to-do item.
    """
    todos_db.append(todo)
    return todo


@app.get("/todos/", response_model=List[Todo])
def read_todos():
    """
        Get a list of all to-do items.

        Returns:
        - List[Todo]: List of all to-do items.
    """
    return todos_db


@app.get("/todos/{todo_id}", response_model=Todo)
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
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
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
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = completed
    return todo


@app.delete("/todos/{todo_id}", response_model=Todo)
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
        raise HTTPException(status_code=404, detail="Todo not found")
    todos_db.remove(todo)
    return todo
