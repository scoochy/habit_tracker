from sqlalchemy.orm import Session
import models, schemas
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

def get_today_habits(db: Session, today: date):
    """
    Get today's habits

    Args:
        db (Session): SQLAlchemy database session.
         today: date : Today's date.

    Returns:
        DB Query Result : The habits filtered for today's date
    """
    return db.query(models.Habit).filter(models.Habit.date == today).all()

def complete_habit(db: Session, habit_id: int):
    """
    Mark a habit as completed by its ID.

    Args:
        db (Session): SQLAlchemy database session.
        habit_id (int): The ID of the habit.

    Returns:
        Habit: The updated Habit object.
    """
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        habit.completed = True
        db.commit()
        db.refresh(habit)
    return habit
