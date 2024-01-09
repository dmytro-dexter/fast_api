from pydantic import BaseModel, Field


class CreateTodoItem(BaseModel):
    title: str = Field(default="Car", max_length=15)
    description: str = Field(default="Wash", max_length=15)
    done: bool = Field(default=False)


class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    done: bool = False


class UpdateTodoItem(BaseModel):
    title: str | None
    description: str | None
    done: bool | None
