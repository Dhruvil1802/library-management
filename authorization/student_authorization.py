import jwt
from datetime import datetime, timedelta
from crud.student_crud import save_token
from sqlalchemy.orm import Session
from models.student_model import Student, StudentToken
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import get_db


SECRET_KEY = "asdfasdfasdf"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10000


from passlib.context import CryptContext

oauth2_scheme_student = OAuth2PasswordBearer(tokenUrl="/student/login")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data: dict, db: Session, token_type:str, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt




def get_user(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):  
        return False
    return user                                                          

def verify_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")
       
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
 
        db_token = db.query(StudentToken).filter(StudentToken.token == token).first()
        if db_token is None or db_token.expires_at < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid")

        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme_student)):

    email = verify_token(db=db, token=token)
    user = get_user(db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user