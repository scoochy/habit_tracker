from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException
from datetime import date

def upsert_habit(db: Session, habit: schemas.HabitCreate):
    """
    Update/Insert a habit

    Args:
        db (Session): SQLAlchemy database session.
        habit: schemas.HabitCreate  : habit name and type

    Returns:
        new_habit : The habits for today
    """
    existing = db.query(models.Habit).filter(models.Habit.type == habit.type).first()
    if existing:
        existing.name = habit.name
        existing.completed = False
        existing.date = date.today()
        db.commit()
        db.refresh(existing)
        return existing
    new_habit = models.Habit(**habit.dict(), completed=False, date=date.today())
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit



def get_today_habits_for_user(db: Session, user_id: str, today: date):
    """
    Get today's habits

    Args:
        db (Session): SQLAlchemy database session.
        user_id:  str
        today: date : Today's date.

    Returns:
        DB Query Result : The habits filtered for today's date
    """
    return db.query(models.Habit).filter_by(user_id=user_id, date=today).all()


def complete_habit(db: Session, habit_id: int):
    
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        habit.completed = True
        db.commit()
        db.refresh(habit)
    return habit
def complete_habit(db: Session, habit_id: int, user_id: str):
    """
    Mark a habit as completed by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        habit_id (int): The ID of the habit.
        user_id: str user's unique id.

    Returns:
        Habit: The updated Habit object.
    """
    habit = db.query(models.Habit).filter_by(id=habit_id, user_id=user_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found for this user")

    habit.completed = True
    db.commit()
    db.refresh(habit)
    return habit


def reset_habits_for_today(db: Session, user_id: str):
    today = date.today()

    # Check if today's habits already exist
    existing = db.query(models.Habit).filter_by(user_id=user_id, date=today).all()
    if existing:
        return existing

    # Get most recent set of habits before today
    last_habits = db.query(models.Habit).filter(
        models.Habit.user_id == user_id,
        models.Habit.date < today
    ).order_by(models.Habit.date.desc()).all()

    new_habits = []
    for habit in last_habits:
        new_habit = models.Habit(
            name=habit.name,
            time=habit.time,
            user_id=user_id,
            date=today,
            completed=False
        )
        db.add(new_habit)
        new_habits.append(new_habit)

    db.commit()
    return new_habits

def get_start_date(db: Session, user_id: str):
    first_habit = db.query(models.Habit).filter_by(user_id=user_id).order_by(models.Habit.date.asc()).first()
    return first_habit.date if first_habit else None

