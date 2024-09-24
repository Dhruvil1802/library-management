from datetime import datetime, timedelta
from authorization.student_authorization import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.student_schemas import StudentBase
from crud import student_crud
from schemas.student_schemas import StudentBase, Token
from models.student_model import Student
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Register a new student
@router.post("/student/registration", response_model=StudentBase, status_code=201)
def register_student(student: StudentBase, db: Session = Depends(get_db)):
    existing_student = student_crud.get_student_by_email(db, email=student.email)  
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    return student_crud.create_student(db=db, student=student)  


# Log in the student and issue a JWT access token
@router.post("/student/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = authenticate_user(db, email=form_data.username, password=form_data.password)  
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        db=db,
        token_type="bearer",
        expires_delta=access_token_expires
    )

    expires_at = datetime.utcnow() + access_token_expires  
    student_crud.save_token(db=db, token=access_token, token_type="bearer", expires_at=expires_at)

    return Token(access_token=access_token, token_type="bearer")


# A protected route accessible only by authenticated students
@router.get("/protected-route")
async def protected_route(current_user: Student = Depends(get_current_user)):

    return {"message": f"Hello, {current_user.email}. You are authenticated!"}