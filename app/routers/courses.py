from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from modelss.student import CourseResponse
from dependencies import pagination,verify_api_key
router=APIRouter(prefix="/courses",tags=["Courses"])
courses = [
    {"id": 1, "name": "Backend", "students": 15},
    {"id": 2, "name": "AI Engineering", "students": 8},
]
@router.get("/")
def get_courses():
    return courses
@router.get("/{id}",response_model=CourseResponse)
def get_course_by_id(id:int):
    for c in courses:
        if c["id"]==id:
            return c
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Course not found!")
