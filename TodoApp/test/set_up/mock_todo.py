import pytest
from sqlalchemy import text

from TodoApp.test.set_up.mock_database import MockedSessionLocal, mock_db_engine
from TodoApp.models import Todos


@pytest.fixture
def get_test_todo():
    test_todo = Todos(
        title="Learn to code",
        description="Need to learn daily",
        priority=5,
        complete=False,
        owner_id=1
    )
    db = MockedSessionLocal()
    db.add(test_todo)
    db.commit()
    db.close()

    yield test_todo

    with mock_db_engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()