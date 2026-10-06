from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status
from ..models import Users
from .auth import bcrypt_context
from .db_utils.db_dependency import db_dependency

from .db_utils.user_dependency import user_dependency

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class UserAuthentication(BaseModel):
    password: str
    new_password: str

class AuthenticatorUserPhoneNumber(BaseModel):
    phone_number: str

def is_no_user(user):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")


@router.get("/get-user", status_code= status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    is_no_user(user)

    return db.query(Users).filter(Users.id == user.get("id")).first()


@router.put("/change-password", status_code= status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_authentication: UserAuthentication):
    is_no_user(user)

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    if not bcrypt_context.verify(user_authentication.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_authentication.new_password)

    db.add(user_model)
    db.commit()

@router.put("/update-phone-number", status_code= status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, authenticated_user: AuthenticatorUserPhoneNumber):
    is_no_user(user)

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    user_model.phone_number = authenticated_user.phone_number

    db.add(user_model)
    db.commit()



    


