from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException, Path, status
from ..models import Todos
from .db_utils.db_dependency import db_dependency
from .db_utils.user_dependency import user_dependency
from sqlalchemy import and_

router = APIRouter()

class TodoRequest(BaseModel):
    title: str = Field(min_length = 3)
    description: str = Field(min_length = 3, max_length = 100)
    priority: int = Field(gt = 0)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Authentication failed")

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Authentication failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
                  .filter(Todos.owner_id == user.get("id")).first()

    # todo_model = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.get("id")).first()

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.post("/todo/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is not None:
        new_todo = Todos(**todo_request.dict(), owner_id =user.get("id"))

        db.add(new_todo)
        db.commit()
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Authenticated failed")


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Authenticated failed")

    todo_model = db.query(Todos)\
        .filter(
            and_(Todos.id == todo_id, Todos.owner_id == user.get("id"))
        ).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt = 0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Authenticated failed")
    filtered_todo = db.query(Todos)\
        .filter(Todos.id == todo_id, Todos.owner_id == user.get("id"))
    todo_model = filtered_todo.first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    filtered_todo.delete()
    db.commit()
