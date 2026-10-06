from fastapi.testclient import TestClient
from fastapi import status

from .set_up.mock_db_utils.mock_db_dependency import override_get_db
from .set_up.mock_db_utils.mock_user_dependency import override_get_current_user
from ..main import app
from ..routers.auth import get_current_user
from ..routers.db_utils.db_dependency import get_db
from .set_up.mock_user import get_test_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_get_user(get_test_user):
    response = client.get("/users/get-user")
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json["id"] == 1
    assert response_json["username"] == "codingwithhari"
    assert response_json["role"] == "admin"
    assert response_json["email"] == "hari@gmail.com"
    assert response_json["phone_number"] == "32676234423"
    assert response_json["is_active"] == True
    assert response_json["first_name"] == "hari"
    assert response_json["last_name"] == "raj"
    assert response_json["is_active"] == True


def test_change_password_success(get_test_user):
    request_data = {
        "password": "testpassword@123#",
        "new_password": "newpassword@123#"
    }
    response = client.put("/users/change-password", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(get_test_user):
    request_data = {
        "password": "wrong_password@123#",
        "new_password": "newpassword@123#"
    }
    response = client.put("/users/change-password", json=request_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_update_phone_number(get_test_user):
    request_data = {
        "phone_number": "1234567891"
    }
    response = client.put("/users/update-phone-number", json=request_data)

    response.status_code = status.HTTP_204_NO_CONTENT