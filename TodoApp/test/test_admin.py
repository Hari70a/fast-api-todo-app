from fastapi.testclient import TestClient
from fastapi import status

from .set_up.mock_database import MockedSessionLocal
from .set_up.mock_db_utils.mock_db_dependency import override_get_db
from .set_up.mock_db_utils.mock_user_dependency import override_get_current_user
from ..models import Todos
from ..routers.db_utils.db_dependency import get_db
from ..routers.db_utils.user_dependency import get_current_user
from ..main import app
from .set_up.mock_todo import get_test_todo

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_admin_todos(get_test_todo):
    response = client.get("/admin/todos")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1, "title": "Learn to code",
                                "description": "Need to learn daily",
                                "priority": 5, "complete": False,
                                "owner_id": 1}]


def test_admin_delete_todo(get_test_todo):
    response = client.delete("/admin/todo/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = MockedSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None
    db.close()