from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, todos, users

app = FastAPI()

# create all the table in DB if not exist
Base.metadata.create_all(bind=engine)

#all routes will be here
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)


# origins = [
#     "http://localhost:5173", 
# ]
# #cors
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )