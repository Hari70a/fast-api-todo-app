from fastapi.testclient import TestClient
from fastapi import status

from .set_up.mock_db_utils.mock_db_dependency import override_get_db
from .set_up.mock_db_utils.mock_user_dependency import override_get_current_user
from ..main import app
from ..routers.db_utils.db_dependency import get_db
from ..routers.auth import get_current_user
from .set_up.mock_database import MockedSessionLocal
from ..models import Todos
from .set_up.mock_todo import get_test_todo

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_read_all_authenticated_todos(get_test_todo):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1, "title": "Learn to code",
                                "description": "Need to learn daily",
                                "priority": 5, "complete": False,
                                "owner_id": 1}]


def test_read_authenticated_todo(get_test_todo):
    response = client.get("/todos/1")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "title": "Learn to code",
                                "description": "Need to learn daily",
                                "priority": 5, "complete": False,
                                "owner_id": 1}


def test_read_authenticated_unavailable_todo(get_test_todo):
    response = client.get("/todos/99")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}



def test_authenticated_create_todo(get_test_todo):
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }

    response = client.post("/todo/create_todo", json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    db = MockedSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()

    print(model)

    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")
    assert model.owner_id == request_data.get("owner_id")
    db.close()


def test_update_todo(get_test_todo):
    request_data = {
        "title": "New title to update for testing purpose",
        "description": "Need to learn daily",
        "complete": False,
        "priority": 5,
        "owner_id": 1
    }

    response = client.put("/todo/1", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = MockedSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")
    assert model.owner_id == request_data.get("owner_id")
    db.close()


def test_update_unavailable_todo(get_test_todo):
    request_data = {
        "title": "New title to update for testing purpose",
        "description": "Need to learn daily",
        "complete": False,
        "priority": 5,
        "owner_id": 1
    }

    response = client.put("/todo/99", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(get_test_todo):
    response = client.delete("/todo/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = MockedSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
    db.close()



def test_delete_todo_unavailable(get_test_todo):
    response = client.delete("/todo/99")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo not found"}