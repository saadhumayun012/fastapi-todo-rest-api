from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

DATABSE_URL = settings.database_url

engine = create_engine(DATABSE_URL)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Create a base class for models to inherit
Base = declarative_base()