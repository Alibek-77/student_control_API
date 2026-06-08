from database import Base
from sqlalchemy import Column,Integer,String,Float
class Student(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100),nullable=False)
    course=Column(String(50),nullable=False)
    grade=Column(Float,nullable=False)
