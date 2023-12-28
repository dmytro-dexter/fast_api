from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class TodoItemDB(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    done = Column(Boolean, default=False)



