from .models import todos_db


def get_todo_by_id(todo_id: int):
    for key, value in todos_db.items():
        if key == todo_id:
            return todos_db[key]
    return None
