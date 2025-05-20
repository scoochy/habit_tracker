from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy import Enum as SqlEnum  # SQLAlchemy Enum type (aliased to avoid conflict with Python's Enum)
from enum import Enum  # Python's standard Enum for defining fixed choices
from  database import Base  # Base class for SQLAlchemy models (from your database setup)

# Define valid habit categories using Python Enum
class HabitType(str, Enum):
    body = "body"
    mind = "mind"
    learn = "learn"

# Define the Habit model mapped to the "habits" table
class Habit(Base):
    __tablename__ = "habits"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing primary key
    name = Column(String, nullable=False)  # Name of the habit (required)
    type = Column(SqlEnum(HabitType), unique=True, nullable=False)  # Enum: one unique habit per type
    completed = Column(Boolean, default=False)  # Tracks if the habit is completed for the day
    date = Column(Date)  # Date associated with the habit (typically today)
    user_id = Column(String, index=True)
