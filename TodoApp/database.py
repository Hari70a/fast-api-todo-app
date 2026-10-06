
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todoApp.db'
# The below one is not working due to the special character '@' in the password.
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Admin@123@localhost/TodoApplicationDatabases'
SQLALCHEMY_DATABASE_URL = URL.create(
    drivername=getenv("PG_DRIVER_NAME"),
    username=getenv("PG_USER"),
    password=getenv("PG_PASSWORD"),
    host=getenv("PG_HOST"),
    port=getenv("PG_PORT"),
    database=getenv("PG_DB"),
)

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args ={"check_same_thread" : False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(
    autocommit= False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()