from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from passlib.context import CryptContext

from app.models import Users
from app.routers.auth import get_current_user #reason added in auth.py (its a dependecy injection)
from app.schemas import PasswordChangeRequest, PhoneNumberRequest
from app.utils import db_dependency

router = APIRouter(
    prefix="/users",
    tags=["user"]
)

#a dependency injection for current user
user_dependency = Annotated[dict, Depends(get_current_user)]
#for hash the password
bcrypt_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#user can see his details
@router.get("/detail", status_code=status.HTTP_200_OK)
def user_details(
    db: db_dependency,
    user: user_dependency
):
    user_model = db.query(Users).filter(Users.id == user.id).first()
    return user_model

#password change
@router.post("/password", status_code=status.HTTP_200_OK)
def change_password(
    db: db_dependency,
    user: user_dependency,
    pwd_change_request: PasswordChangeRequest
):
    user_model = db.query(Users).filter(Users.id == user.id).first()

    if not bcrypt_pwd_context.verify(pwd_change_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    if pwd_change_request.password == pwd_change_request.new_password:
        raise HTTPException(status_code=400, detail="New password must be differend from old password")
    
    user_model.hashed_password =  bcrypt_pwd_context.hash(pwd_change_request.new_password)
    db.commit()

#add phone number ( the number is added after the table is create through alembic)
@router.post("/phone", status_code=status.HTTP_200_OK)
def phone_number(
        phone_number_request: PhoneNumberRequest,
        db: db_dependency,
        user: user_dependency
):
    user_model = db.query(Users).filter(Users.id == user.id).first()
    user_model.phone_number = phone_number_request.phone_number

    db.commit()
    db.refresh(user_model)

    return {"message": "phone added successfully"}