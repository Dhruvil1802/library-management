
from sqlalchemy.orm import Session


from models import lib_admin_model
from schemas.lib_admin_schemas import LibAdminBasePassword

from datetime import datetime
from passlib.context import CryptContext

def get_lib_admin_by_email(db: Session, email: str):
    return db.query(lib_admin_model.LibAdmin).filter(lib_admin_model.LibAdmin.email == email).first()

def create_lib_admin(db: Session, lib_admin: LibAdminBasePassword,access_token):
    hashed_password = get_password_hash(lib_admin.password)  
    lib_admin.password = hashed_password  
    new_lib_admin = lib_admin_model.LibAdmin(**lib_admin.dict())
    db.add(new_lib_admin)
    db.commit()
    db.refresh(new_lib_admin)
    print(new_lib_admin)
    return new_lib_admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def save_token(db: Session, token: str, token_type: str, expires_at: datetime):
    db_token = lib_admin_model.LibAdminToken(token=token, token_type=token_type, expires_at=expires_at)
    db.add(db_token)  
    db.commit()
    db.refresh(db_token)
    return db_token