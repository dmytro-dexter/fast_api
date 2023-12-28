from pydantic import BaseModel


class CreateTodoItem(BaseModel):
    title: str
    description: str
    done: bool = False


class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False


class UpdateTodoItem(BaseModel):
    title: str | None
    description: str | None
    done: bool | None
