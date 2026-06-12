from fastapi import APIRouter,Depends,HTTPException,status,BackgroundTasks
from schemas import CourseCreate,CourseResponse
from database import get_db
from sqlalchemy.orm import Session
from models import Course
from background_tasks import write_log_for_course
import logging
router=APIRouter(
    tags=["Courses"],
    prefix="/courses"
)
logger=logging.getLogger(__name__)
@router.get("/",response_model=list[CourseResponse])
def get_courses(db:Session=Depends(get_db)):
    courses=db.query(Course).all()
    logger.info(f"Returned {list(courses)} courses")
    return courses
@router.get("/{id}",response_model=CourseResponse)
def get_course_by_id(id:int,db:Session=Depends(get_db)):
    course=db.query(Course).filter(Course.id==id).first()
    if not course:
        logger.error(f"Course {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Course not found")
    return course
@router.post("/",response_model=CourseResponse,status_code=201)
def create_user(course:CourseCreate,background_tasks:BackgroundTasks,db:Session=Depends(get_db)):
    new_user=Course(**course.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Student created: id={new_user.id}, name={new_user.name}")
    background_tasks.add_task(write_log_for_course,"course created",course)
    return new_user