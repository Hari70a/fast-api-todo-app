from datetime import timedelta
from fastapi import HTTPException, status

import pytest
from jose import jwt

from .set_up.mock_database import MockedSessionLocal
from .set_up.mock_db_utils.mock_db_dependency import override_get_db
from .set_up.mock_user import get_test_user
from ..main import app
from ..routers.auth import authenticate_user, SECRET_KEY, ALGORITHM, create_access_token, get_current_user

from ..routers.db_utils.db_dependency import get_db

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(get_test_user):
    db = MockedSessionLocal()

    validate_available_user = authenticate_user(get_test_user.username, "testpassword@123#", db)

    assert validate_available_user is not None
    assert validate_available_user.username == get_test_user.username

    non_existent_user = authenticate_user("wrongusername", "testpassword@123#", db)

    assert non_existent_user is False

    unverified_user = authenticate_user(get_test_user.username, "wrongpassword", db)

    assert non_existent_user is False


def test_create_access_token():
    username = "codingwwithhari"
    user_id = 1
    user_role = "user"
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, user_role, expires_delta)

    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options = {"verify_signature": False})

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["user_role"] == user_role

@pytest.mark.asyncio
async def test_get_current_user():
    username = "codingwwithhari"
    user_id = 1
    user_role = "user"
    encode = {"sub": username, "id": user_id, "user_role": user_role}

    token = jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)

    user = await get_current_user(token)

    assert user == { "username": username, "id": user_id, "user_role": user_role }


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = { "sub": "codingwithhari" }

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exception:
        await get_current_user(token)

    assert exception.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exception.value.detail == "Could not validate the user"