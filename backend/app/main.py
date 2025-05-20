from fastapi import FastAPI, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date
import models, schemas, crud
from database import engine, SessionLocal
from models import Habit

import os

models.Base.metadata.create_all(bind=engine)

frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../frontend")

app = FastAPI(debug=True)

# Allow all origins for dev (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8000", "http://127.0.0.1:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Serve static files (like CSS, JS, images) from the frontend folder
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Route to serve the index.html file
@app.get("/", response_class=HTMLResponse)
def read_index():
    with open(os.path.join(frontend_path, "index.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)
    
# Route to serve the set.html file
@app.get("/set", response_class=HTMLResponse)
def read_set():
    with open(os.path.join(frontend_path, "set.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)
    
# Route to serve the set.html file
@app.get("/today", response_class=HTMLResponse)
def read_today():
    with open(os.path.join(frontend_path, "today.html"), "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)
    
# Route to serve the complete.html file
@app.get("/complete", response_class=HTMLResponse)
def read_complete():
    with open(os.path.join(frontend_path, "complete.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Route: Create a new habit
@app.post("/habits/", response_model=schemas.HabitOut)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    return crud.upsert_habit(db, habit)

# Get today's habits
@app.get("/habits/", response_model=list[schemas.HabitOut])
def read_today_habits(user_id: str = Query(...), db: Session = Depends(get_db)):
    return crud.get_today_habits_for_user(db, user_id, date.today())

#MArk habit as completed
@app.post("/habits/{habit_id}/complete", response_model=schemas.HabitOut)
def complete_habit(habit_id: int, user_id: str = Query(...), db: Session = Depends(get_db)):
    return crud.complete_habit(db, habit_id, user_id)

#reset habits
@app.post("/habits/reset", response_model=list[schemas.HabitOut])
def reset_daily_habits(user_id: str = Query(...), db: Session = Depends(get_db)):
    return crud.reset_habits_for_today(db, user_id)

#habit start date
@app.get("/habits/start-date")
def get_habit_start_date(user_id: str = Query(...), db: Session = Depends(get_db)):
    start_date = crud.get_start_date(db, user_id)
    return {"start_date": start_date}
