# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date
import models, schemas, crud
from database import engine, SessionLocal
from models import Habit

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# Dependency: get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route: Create a new habit
@app.post("/habits/", response_model=schemas.HabitOut)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    return crud.upsert_habit(db, habit)

# Route: Get today’s habits
@app.get("/habits/", response_model=list[schemas.HabitOut])
def read_today_habits(db: Session = Depends(get_db)):
    return crud.get_today_habits(db, date.today())

# Route: Mark a habit as completed
@app.post("/habits/{habit_id}/complete", response_model=schemas.HabitOut)
def complete_habit(habit_id: int, db: Session = Depends(get_db)):
    return crud.complete_habit(db, habit_id)
