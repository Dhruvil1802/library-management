from sqlalchemy import Column, Integer, String, DateTime
from database import Base  
from datetime import datetime
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"


    student_id = Column(Integer, primary_key=True, index=True)

    email = Column(String(length=255), unique=True, index=True) 

    password = Column(String(length=255))  

    name = Column(String(length=255))

    borrowed_books = relationship("BorrowedBook", back_populates="student")  # Update to reference BorrowedBook

class StudentToken(Base):
    __tablename__ = "student_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(256), unique=True, nullable=False)
    token_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)