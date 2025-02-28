# database/db_setup.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file location (relative to the project root)
SQLALCHEMY_DATABASE_URL = "sqlite:///./aadhar_system.db"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Create a session local class for DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()
