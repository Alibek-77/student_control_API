from pydantic import Field,BaseModel
from typing import Optional
class StudentCreate(BaseModel):
    name:str=Field(min_length=2)
    course:str
    grade:float=Field(ge=0,le=100)
class StudentUpdate(BaseModel):
    name:Optional[str]=None
    course:Optional[str]=None
    grade:Optional[float]=None
class StudentResponse(BaseModel):
    id:int
    name:str
    course:str
    grade:float
class CourseResponse(BaseModel):
    id:int
    name:str
    students:int