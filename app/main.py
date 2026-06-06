from fastapi import FastAPI,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import Field,BaseModel
from typing import Optional
from routers import students,courses
import os
from dotenv import load_dotenv
load_dotenv()
allowed_origins=os.getenv("ALLOWED_ORIGINS","http://localhost:3000").split(",")
app=FastAPI(title="Student API",description="API for control students",version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(students.router)
app.include_router(courses.router)
@app.get("/",tags=["Health"])
def health_check():
    return {"status":"ok","version":"1.0.0"}
