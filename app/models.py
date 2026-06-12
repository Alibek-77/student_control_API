from database import Base
from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship
class Course(Base):
    __tablename__="courses"
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String(50),nullable=False)
    description=Column(String(500))
    students=relationship("Student",back_populates="course")
class Student(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(100),nullable=False)
    grade=Column(Float,nullable=False)
    course_id=Column(Integer,ForeignKey("courses.id"),nullable=False)
    course=relationship("Course",back_populates="students")