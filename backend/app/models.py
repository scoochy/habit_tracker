from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy import Enum as SqlEnum
from enum import Enum  # Python enum
from database import Base

class HabitType(str, Enum):
    body = "body"
    mind = "mind"
    learn = "learn"

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(SqlEnum(HabitType), unique=True, nullable=False)
    completed = Column(Boolean, default=False)
    date = Column(Date)
