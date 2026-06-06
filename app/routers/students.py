from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from modelss.student import StudentResponse,StudentCreate,StudentUpdate
from dependencies import pagination,verify_api_key
students = [
    {"id": 1, "name": "Alibek", "course": "Backend", "grade": 95},
    {"id": 2, "name": "Aizat", "course": "AI", "grade": 88},
]
router=APIRouter(
    prefix="/students",
    tags=["Students"]
)
@router.get("/")
def get_users(pages:dict=Depends(pagination)):
    start=pages["skip"]
    end=pages["skip"]+pages["limit"]
    return students[start:end]
@router.get("/{student_id}")
def get_student_by_id(student_id:int):
    for s in students:
        if s["id"]==student_id:
            return s
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
@router.post("/",status_code=201,response_model=StudentResponse)
def create_user(student:StudentCreate,key:str=Depends(verify_api_key)):
    new_id=max([s["id"] for s in students])+1
    new_user={"id":new_id,**student.model_dump()}
    students.append(new_user)
    return new_user
@router.put("/{id}")
def replace_user(id:int,student:StudentCreate,key:str=Depends(verify_api_key)):
    for i,s in enumerate(students):
        if s["id"]==id:
            students[i]={"id":id,**student.model_dump()}
            return students[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found!")
@router.patch("/{id}",response_model=StudentResponse)
def update_user(id:int,student:StudentUpdate,key:str=Depends(verify_api_key)):
    for i,s in enumerate(students):
        if s["id"]==id:
            update_student=student.model_dump(exclude_none=True)
            s.update(update_student)
            return s
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
@router.delete("/{id}",status_code=204)
def delete_user(id:int,key:str=Depends(verify_api_key)):
    for i,s in enumerate(students):
        if s["id"]==id:
            students.pop(i)
            return 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found!")
