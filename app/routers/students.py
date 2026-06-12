from fastapi import Depends,HTTPException,status,APIRouter,BackgroundTasks,Request
from schemas import StudentResponse,StudentCreate,StudentUpdate
from dependencies import pagination,verify_api_key
from background_tasks import write_log
from sqlalchemy.orm import Session,joinedload
from database import get_db
from models import Student,Course
import time,logging
logger=logging.getLogger(__name__)
router=APIRouter(
    prefix="/students",
    tags=["Students"]
)
@router.get("/",response_model=list[StudentResponse])
def get_users(db:Session=Depends(get_db)):
    students=db.query(Student).options(joinedload(Student.course)).all()
    logger.info(f"Returned {len(students)} students")
    return students
@router.get("/{student_id}",response_model=StudentResponse)
def get_student_by_id(student_id:int,db:Session=Depends(get_db)):
    student=db.query(Student).options(joinedload(Student.course)).filter(Student.id==student_id).first()
    if not student:
        logger.error(f"Student {student_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    return student
@router.post("/",status_code=201,response_model=StudentResponse)
def create_user(student:StudentCreate,background_tasks:BackgroundTasks,key:str=Depends(verify_api_key),db:Session=Depends(get_db)):
    course=db.query(Course).filter(Course.id==student.course_id).first()
    if not course:
        logger.error(f"Course {student.course_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Course not found")
    new_student=Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    logger.info(f"Student created:id={new_student.id} name={student.name}")
    background_tasks.add_task(write_log,"student created",student)
    return student
@router.put("/{id}")
def replace_user(id:int,student:StudentCreate,db:Session=Depends(get_db),key:str=Depends(verify_api_key)):
    db_user=db.query(Student).filter(Student.id==id).first()
    if not db_user:
        logger.error(f"Student {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found!")
    course = db.query(Course).filter(Course.id == student.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for field,value in student.model_dump().items():
        setattr(db_user,field,value)
    db.commit()
    db.refresh(db_user)
    return db_user
@router.patch("/{id}",response_model=StudentResponse)
def update_user(id:int,student:StudentUpdate,db:Session=Depends(get_db),key:str=Depends(verify_api_key)):
    db_user=db.query(Student).filter(Student.id==id).first()
    if not db_user:
        logger.error(f"Student {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    for field,value in student.model_dump(exclude_none=True).items():
        setattr(db_user,field,value)
    db.commit()
    db.refresh(db_user)
    return db_user
@router.delete("/{id}",status_code=204)
def delete_user(id:int,key:str=Depends(verify_api_key),db:Session=Depends(get_db)):
    db_user=db.query(Student).filter(Student.id==id).first()
    if not db_user:
        logger.error(f"Student {id} not found") 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found!")
    db.delete(db_user)
    db.commit()
    logger.info(f"Student {id} deleted!")