# 🎓 Student API
 
A REST API for managing students built with FastAPI. Features request logging, background tasks, and clean project architecture.
 
## Features
 
- Full CRUD for students and courses
- API key authentication via headers
- Pagination with configurable skip/limit
- Request timing middleware
- Background task logging to JSON
- File-based application logs
## Tech Stack
 
- **FastAPI** — REST API framework
- **Pydantic** — data validation
- **python-dotenv** — environment config
- **uvicorn** — ASGI server
## Project Structure
 
```
student_api/
├── app/
│   ├── main.py              # app setup, middleware, logging
│   ├── dependencies.py      # shared dependencies (auth, pagination)
│   ├── background_tasks.py  # background task functions
│   ├── routers/
│   │   ├── students.py      # student endpoints
│   │   └── courses.py       # course endpoints
│   └── modelss/
│       └── student.py       # Pydantic models
├── logs/                    # auto-created
│   ├── app.log              # application logs
│   └── activity.json        # background task logs
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
 
**4. Create `.env` file**
```
API_KEY=secret123
ALLOWED_ORIGINS=http://localhost:3000
```
 
**5. Run the server**
```bash
uvicorn app.main:app --reload
```
 
## API Endpoints
 
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Health check | — |
| GET | `/students/` | List students (paginated) | — |
| GET | `/students/{id}` | Get student by ID | — |
| POST | `/students/` | Create student | ✓ |
| PUT | `/students/{id}` | Replace student | ✓ |
| PATCH | `/students/{id}` | Update student | ✓ |
| DELETE | `/students/{id}` | Delete student | ✓ |
| GET | `/courses/` | List courses | — |
| GET | `/courses/{id}` | Get course by ID | — |
 
## Authentication
 
Protected endpoints require an `api-key` header:
```
api-key: secret123
```
 
## Pagination
 
```
GET /students/?skip=0&limit=10
```
 
## Documentation
 
Interactive API docs available at `http://localhost:8000/docs`
 
## Requirements
 
```
fastapi
uvicorn
pydantic
python-dotenv
```
 
> **Note:** Database integration (PostgreSQL + SQLAlchemy) coming soon.