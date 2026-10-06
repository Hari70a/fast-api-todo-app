from fastapi import APIRouter, HTTPException, Path
from starlette import status
from ..models import Todos
from .db_utils.db_dependency import db_dependency

from .db_utils.user_dependency import user_dependency

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

def is_admin(user):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")


@router.get("/todos", status_code= status.HTTP_200_OK)
async def get_todos(user: user_dependency, db: db_dependency):
    is_admin(user)

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    is_admin(user)

    filtered_todo = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.get("id"))

    todo_model = filtered_todo.first()

    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    filtered_todo.delete()
    db.commit()