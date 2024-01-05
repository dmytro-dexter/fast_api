from fastapi.testclient import TestClient
from ...main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..models import TodoItemDB

from ..database import Base
from ..deps import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_todos():
    with TestingSessionLocal() as test_db:
        test_db.add_all([
            TodoItemDB(title="Todo 1", description="Description 1", done=False),
            TodoItemDB(title="Todo 2", description="Description 2", done=False),
        ])
        test_db.commit()

    response = client.get("/todos/")
    assert response.status_code == 200

    todos = response.json()
    assert len(todos) == 2
    assert todos[0]["title"] == "Todo 1"
    assert todos[1]["description"] == "Description 2"


def test_read_todo():
    with TestingSessionLocal() as test_db:
        test_db.add(TodoItemDB(title="Test Todo", description="Test Description", done=False))
        test_db.commit()

        todo_id = test_db.query(TodoItemDB).first().id
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200

    todo = response.json()
    assert todo["title"] == "Test Todo"
    assert todo["description"] == "Test Description"


def test_read_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404


def test_create_todo():
    todo_data = {"title": "Test Todo", "description": "Test Description", "done": False}
    response = client.post("/todos/", json=todo_data)

    assert response.status_code == 200
    created_todo = response.json()
    assert created_todo["title"] == todo_data["title"]
    assert created_todo["description"] == todo_data["description"]
    assert created_todo["done"] == todo_data["done"]


def test_create_todo_invalid_data():
    invalid_todo_data = {"title": "Test Todo"}
    response = client.post("/todos/", json=invalid_todo_data)

    assert response.status_code == 422


def test_update_todo():
    with TestingSessionLocal() as test_db:
        test_db.add(TodoItemDB(title="Test Todo", description="Test Description", done=False))
        test_db.commit()

        todo_id = test_db.query(TodoItemDB).first().id

    update_data = {"title": "Update Title", "description": "Update Description", "done": True}
    response = client.put(f"/todos/{todo_id}", json=update_data)
    assert response.status_code == 200

    updated_todo = response.json()
    assert updated_todo["title"] == update_data["title"]
    assert updated_todo["description"] == update_data["description"]
    assert updated_todo["done"] == update_data["done"]


def test_update_todo_not_found():
    update_data = {"title": "Updated Title", "description": "Updated Description", "done": True}
    response = client.put("/todos/999", json=update_data)
    assert response.status_code == 404


def test_delete_todo():
    with TestingSessionLocal() as test_db:
        test_db.add(TodoItemDB(title="Test Todo", description="Test Description", done=False))
        test_db.commit()

        todo_id = test_db.query(TodoItemDB).first().id

    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200

    with TestingSessionLocal as test_db:
        deleted_todo = test_db.query(TodoItemDB).get(todo_id)
        assert deleted_todo is None


def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
