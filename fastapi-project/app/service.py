from .models import todos_db


def get_todo_by_id(todo_id: int):
    for element in todos_db:
        if element.id == todo_id:
            return element
    return None