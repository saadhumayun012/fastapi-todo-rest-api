from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import Annotated

from app.models import Todos
from app.routers.auth import get_current_user #reason added in auth.py (its a dependecy injection)
from app.schemas import TodoRequest
from app.utils.dependency import db_dependency

router = APIRouter()


#a dependency injection for current user
user_dependency = Annotated[dict, Depends(get_current_user)]


#get all todos
@router.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos(
    db: db_dependency,
    user: user_dependency
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return db.query(Todos).filter(Todos.owner_id == user.id).all()

#get todo based upon the id
@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def get_todo_by_id(
    db: db_dependency,
    user: user_dependency,
    todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="No Todo Found on the given id")
    
    return todo_model

#post the todo or add the todo
@router.post("/add_todo", status_code=status.HTTP_201_CREATED)
def add_todo(
    db: db_dependency,
    user: user_dependency,
    todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id = user.id)
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

#put or update the existing todo
@router.put("/update_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(
    db: db_dependency,
    user: user_dependency,
    todo_request: TodoRequest,
    todo_id: int
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo_model = db.query(Todos)\
    .filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.id)\
    .first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="No Todo Found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

#delete the todo
@router.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
  db: db_dependency,
  user: user_dependency,
  todo_id: int      
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    todo_model = db.query(Todos)\
    .filter(Todos.id == todo_id)\
    .filter(Todos.owner_id == user.id)\
    .first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="No Todo Found")
    
    db.delete(todo_model)
    db.commit()