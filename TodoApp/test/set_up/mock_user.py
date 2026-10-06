import pytest
from sqlalchemy import text

from .mock_database import MockedSessionLocal, mock_db_engine
from ...models import Users
from ...routers.auth import bcrypt_context


@pytest.fixture
def get_test_user():
    test_user = Users(
        username="codingwithhari",
        role="admin",
        email="hari@gmail.com",
        phone_number="32676234423",
        is_active=True,
        first_name="hari",
        last_name="raj",
        hashed_password=bcrypt_context.hash("testpassword@123#")
    )
    db = MockedSessionLocal()
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    db.close()

    yield test_user

    with mock_db_engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()