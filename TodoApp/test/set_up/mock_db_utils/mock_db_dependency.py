from ..mock_database import MockedSessionLocal


def override_get_db():
    mock_db = MockedSessionLocal()
    try:
        yield mock_db
    finally:
        mock_db.close()