from sqlalchemy.orm import Session
from models.student_model import StudentToken,Student
from schemas.student_schemas import StudentBase

from datetime import datetime
from passlib.context import CryptContext



def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

def create_student(db: Session, student: StudentBase):
    hashed_password = get_password_hash(student.password)  
    student.password = hashed_password  
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def save_token(db: Session, token: str, token_type: str, expires_at: datetime):
    db_token = StudentToken(token=token, token_type=token_type, expires_at=expires_at)
    db.add(db_token)  
    db.commit()
    db.refresh(db_token)
    return db_token

def delete_token(db: Session, token: str):
    db_token = db.query(StudentToken).filter(StudentToken.token == token).first()
    if db_token:
        db.delete(db_token)
        db.commit()
        return True  
    return False  