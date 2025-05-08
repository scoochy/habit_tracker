# habit_tracker
 
NewDawn:
A minimalist habit tracker focused on morning routine consistency in Body, Mind, and Learning.

🔧 Features
Track 3 daily habits one for each type: body, mind, and learn

FastAPI backend with SQLite + SQLAlchemy

React Native mobile frontend

RESTful API with Swagger docs

⚙️ Tech Stack  

Backend: 	Python, FastAPI, SQLAlchemy, SQLite  
Frontend: 	React Native, Expo  
API Docs:	Swagger (built-in with FastAPI)  
Testing:	Pytest (planned)  


## 🚀 Setup Instructions


Follow the steps below to set up the project environment.

### 1. Clone repository

```
git clone https://github.com/scoochy/habit_tracker.git
cd habit_tracker
```

### 2. Create and Activate a Virtual Environment


```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the API server

```bash
uvicorn main:app --reload
```