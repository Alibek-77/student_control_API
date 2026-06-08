# 🎓 Student API v2.0
 
A production-ready REST API for managing students built with FastAPI and PostgreSQL. Features real database persistence, request logging, background tasks, and clean project architecture.
 
## What's New in v2.0
 
- **PostgreSQL** — data persists between server restarts
- **SQLAlchemy ORM** — database operations through Python objects
- **Real transactions** — safe data operations with rollback support
## Tech Stack
 
- **FastAPI** — REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM and database toolkit
- **Pydantic** — data validation and schemas
- **python-dotenv** — environment config
- **uvicorn** — ASGI server
## Project Structure
 
```
student_api/
├── main.py              # app setup, middleware, logging
├── database.py          # database connection and session
├── models.py            # SQLAlchemy models (tables)
├── schemas.py           # Pydantic models (validation)
├── dependencies.py      # shared dependencies (auth, pagination)
├── background_tasks.py  # background task functions
├── routers/
│   └── students.py      # student endpoints
├── logs/                # auto-created
│   ├── app.log          # application logs
│   └── activity.json    # background task logs
├── .env.example
├── requirements.txt
└── .gitignore
```
 
## Setup
 
**1. Clone the repository**
```bash
git clone https://github.com/your-username/student-api.git
cd student-api
```
 
**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
```
 
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
 
**4. Create PostgreSQL database**
```sql
CREATE DATABASE student_db;
```
 
**5. Create `.env` file**
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/student_db
API_KEY=secret123
ALLOWED_ORIGINS=http://localhost:3000
```
 
**6. Run the server**
```bash
uvicorn main:app --reload
```
 
Tables are created automatically on first run.
 
## API Endpoints
 
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Health check | — |
| GET | `/students/` | List all students | — |
| GET | `/students/{id}` | Get student by ID | — |
| POST | `/students/` | Create student | ✓ |
| PUT | `/students/{id}` | Replace student | ✓ |
| PATCH | `/students/{id}` | Update student fields | ✓ |
| DELETE | `/students/{id}` | Delete student | ✓ |
 
## Authentication
 
Protected endpoints require an `api-key` header:
```
api-key: secret123
```
 
## How It Works
 
### Database Layer
Each request gets its own database session via `get_db()` dependency. Sessions are automatically closed after every request — even on errors.
 
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
 
### Background Tasks
After creating a student, a background task logs the activity to `logs/activity.json` — without making the client wait.
 
### Middleware
Every request is timed and logged:
```
→ POST http://localhost:8000/students
← 201 in 0.023 sec
```
 
## Documentation
 
Interactive API docs: `http://localhost:8000/docs`
 
## Requirements
 
```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
python-dotenv
```