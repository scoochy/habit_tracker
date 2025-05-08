# app/schemas.py
from pydantic import BaseModel
from typing import Literal
from datetime import date

class HabitBase(BaseModel):
    name: str
    type: Literal["body", "mind", "learn"]

class HabitCreate(HabitBase):
    name: str
    type: Literal["body", "mind", "learn"]

class HabitOut(HabitCreate):
    id: int
    name: str
    completed: bool
    date: date

    class Config:
        orm_mode = True

