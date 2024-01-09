from fastapi.testclient import TestClient
from ... import main

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..models import TodoItemDB


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


def test_read_todos(test_db):
    with test_db as db:
        db.add_all([
            TodoItemDB(title="Todo 1", description="Description 1", done=False),
            TodoItemDB(title="Todo 2", description="Description 2", done=False),
        ])
        db.commit()

    client = TestClient(main.app)
    response = client.get("/todos/")
    assert response.status_code == 200

    todos = response.json()
    assert len(todos) == 2
    assert todos[0]["title"] == "Todo 1"
    assert todos[1]["description"] == "Description 2"


def test_read_todo(test_db):
    with test_db as db:
        todo_model = TodoItemDB(title="Test Title", description="Test Description", done=False)
        db.add(todo_model)
        db.commit()

    client = TestClient(main.app)
    response = client.get(f"/todos/{todo_model.id}")

    assert response.status_code == 200

    todo = response.json()
    assert todo["title"] == "Test Title"
    assert todo["description"] == "Test Description"
    assert todo["done"] == False


def test_create_todo(test_db):
    client = TestClient(main.app)
    todo_data = {"title": "New Todo", "description": "New Description", "done": True}
    response = client.post("/todos/", json=todo_data)

    assert response.status_code == 200

    created_todo = response.json()
    assert created_todo["title"] == "New Todo"
    assert created_todo["description"] == "New Description"
    assert created_todo["done"] == True

    with test_db as db:
        created_todo_db = db.query(TodoItemDB).filter_by(id=created_todo["id"]).first()
        assert created_todo_db is not None
        assert created_todo_db.title == "New Todo"
        assert created_todo_db.description == "New Description"
        assert created_todo_db.done == True


def test_update_todo(test_db):
    with test_db as db:
        todo_model = TodoItemDB(title="Test Todo", description="Test Description", done=False)
        db.add(todo_model)
        db.commit()

    client = TestClient(main.app)
    update_data = {"title": "Updated Title", "description": "Updated Description", "done": True}
    response = client.put(f"/todos/{todo_model.id}", json=update_data)

    assert response.status_code == 200

    updated_todo = response.json()
    assert updated_todo["title"] == "Updated Title"
    assert updated_todo["description"] == "Updated Description"
    assert updated_todo["done"] == True

    with test_db as db:
        updated_todo_db = db.query(TodoItemDB).filter_by(id=todo_model.id).first()
        assert updated_todo_db is not None
        assert updated_todo_db.title == "Updated Title"
        assert updated_todo_db.description == "Updated Description"
        assert updated_todo_db.done == True


def test_delete_todo(test_db):
    with test_db as db:
        todo_model = TodoItemDB(title="Test Title", description="Test Description", done=False)
        db.add(todo_model)
        db.commit()

    client = TestClient(main.app)
    response = client.delete(f"/todos/{todo_model.id}")

    assert response.status_code == 200

    with test_db as db:
        deleted_todo_db = db.query(TodoItemDB).filter_by(id=todo_model.id).first()
        assert deleted_todo_db is None


def test_delete_todo_not_found():
    client = TestClient(main.app)
    response = client.delete("/todos/999")

    assert response.status_code == 404
