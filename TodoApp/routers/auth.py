from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from ..models import Users
from .db_utils.db_dependency import db_dependency
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "wsTuxls7jiIMeGACvtzehDU1FghTlHK8SsgcJ0NnmQwtyhIwtIdN9gZT3h4q+7Xby55tn2x+4q25RxWfBy5CNw=="
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt_sha256","bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

class Token(BaseModel):
    token_type: str
    access_token: str

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username ==
    username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, user_role: str, expires_delta: timedelta):
    encode = { "sub": username, "id":  user_id, "user_role": user_role }
    expiration_time = datetime.now(timezone.utc) + expires_delta

    encode.update({"exp": expiration_time })

    return jwt.encode(encode, SECRET_KEY, algorithm = ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload =  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role= payload.get("user_role")

        if username is None or user_id is None:
           raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Could not validate the user")

        return { "username": username, "id": user_id, "user_role": user_role }

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user")



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model =  Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        role = create_user_request.role,
        phone_number = create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_with_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if user:
        token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

        return { "access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate the user")
