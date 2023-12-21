from pydantic import BaseModel


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
