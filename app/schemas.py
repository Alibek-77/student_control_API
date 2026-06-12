from pydantic import Field,BaseModel
from typing import Optional,List
class CourseResponse(BaseModel):
    id:int
    name:str
    description:Optional[str]=None
    model_config={"from_attributes":True}
class CourseCreate(BaseModel):
    name:str
    description:Optional[str]=None
class StudentCreate(BaseModel):
    name:str=Field(min_length=2)
    grade:float=Field(ge=0,le=100)
    course_id:int
class StudentUpdate(BaseModel):
    name:Optional[str]=None
    course_id:Optional[int]=None
    grade:Optional[float]=None
class StudentResponse(BaseModel):
    id:int
    name:str
    course:CourseResponse
    grade:float
    model_config={"from_attributes":True}
class CourseWithStudents(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    students: List["StudentResponse"] = []
    model_config = {"from_attributes": True}
