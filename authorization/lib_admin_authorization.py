                                                     

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.lib_admin_model import LibAdmin, LibAdminToken
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import get_db

SECRET_KEY = "asdfasdfasdf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10000


oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="/lib_admin/login")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, db: Session, token_type: str, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_admin_by_email(db: Session, email: str):
    return db.query(LibAdmin).filter(LibAdmin.email == email).first()

def authenticate_admin(db: Session, email: str, password: str):
    admin = get_admin_by_email(db, email)
    if not admin or not verify_password(password, admin.password):
        return False
    return admin

def verify_admin_token(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        db_token = db.query(LibAdminToken).filter(LibAdminToken.token == token).first()
        if not db_token or db_token.expires_at < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid")
        
        return email
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

def get_current_admin(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme_admin)):
    email = verify_admin_token(db, token)
    admin = get_admin_by_email(db, email)
    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin
