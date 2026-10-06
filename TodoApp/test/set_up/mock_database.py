from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from TodoApp.database import Base

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./testing.db"

mock_db_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread" : False},
    poolclass=StaticPool
)

MockedSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=mock_db_engine
)

Base.metadata.create_all(bind=mock_db_engine)