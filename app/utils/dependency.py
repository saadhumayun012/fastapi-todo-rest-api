from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from app.database import SessionLocal

#Dependency Injection -> DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#a vaiabel (type hint) for db depency injection 
db_dependency = Annotated[Session, Depends(get_db)]