from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer # OAuth2PasswordBearer extract the token form header ( i am removing this now i change the procedure and save the token in the cookies)
from typing import Annotated
from passlib.context import CryptContext #use to hashed the password
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.config import settings
from app.models import Users
from app.schemas import CreateUserRequest
from app.utils import db_dependency

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

#a varuabel fro oauthbearer (Dont NEED WHEN I DONT SAVE THE TOKEN IN COOKIE)
oauth_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

#hash the password
bcrypt_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#I should have placed the "create_access_token" and "verify_token functions" in the utils directory, 
# and the get_current_user function in the utils/dependency.py file. 
# However, since I am still learning, I have left them here for convenience."

#create the access token
def create_access_token(data: dict):
    to_encode = data.copy()

    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

#token verififcation funtion
def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("id")
        if user_id is None:
            raise ValueError("Invalid token")
        return {"user_id": user_id}
    except JWTError:
        raise ValueError("Invalid token")

#use it as dependecy injection it return the user as a object after verifying the token    
def get_current_user(
    # request: Request,
    db: db_dependency,
    token: Annotated[str, Depends(oauth_bearer)]
):
    # token = request.cookies.get("access_token")

    # if not token:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        token_data = verify_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = db.query(Users).filter(Users.id == token_data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
    

#create the user and add it into db
@router.post("/create_user", status_code=status.HTTP_201_CREATED)
def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest
):
    user = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_pwd_context.hash(create_user_request.password), #password is encrypted
        role = create_user_request.role,
        is_active = True,
        phone_number = create_user_request.phone_number
    )

    if db.query(Users).filter((Users.email == user.email) | (Users.username == user.username)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username is already registered")

    db.add(user)
    db.commit()
    db.refresh(user)

#this is the login route means from there i get the token
@router.post("/login")
def login_for_access_token( 
    # response: Response,
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = db.query(Users).filter(Users.username == form_data.username).first()

    if user is None or not bcrypt_pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    
    token = create_access_token(data={"id": user.id})

    #saving the token in cookies
    # response.set_cookie(
    #     key="access_token",
    #     value=token,
    #     httponly=True,
    #     secure=True,
    #     samesite="lax"
    # )
    # return {"message": "Login successfully"}

    return {"access_token": token, "type": "Bearer"}

#logout routte
# @router.post("/logout",status_code=status.HTTP_200_OK)
# def logout(
#     response: Response
# ):
#     response.delete_cookie(
#         key="access_token",
#         httponly=True,
#         samesite="lax",
#         secure=False
#     )

#     return {"message": "Logged out successfully"}

    
    