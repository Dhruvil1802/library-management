from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from database import SessionLocal, get_db
from models.lib_admin_model import LibAdmin
from schemas.lib_admin_schemas import  LibAdminBasePassword, LibAdminBaseToken,Token
from crud import lib_admin_crud
from authorization.lib_admin_authorization import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_admin, create_access_token, get_current_admin

from fastapi.security import OAuth2PasswordRequestForm

import jwt

router = APIRouter()


# Register a new library admin
@router.post("/lib_admin/registration", response_model=LibAdminBaseToken, status_code=201)
def register_lib_admin(lib_admin:LibAdminBasePassword , db: Session = Depends(get_db)):
    existing_lib_admin = lib_admin_crud.get_lib_admin_by_email(db, email=lib_admin.email)
    if existing_lib_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": lib_admin.email},
        db=db,
        token_type="bearer",
        expires_delta=access_token_expires
    )

    expires_at = datetime.utcnow() + access_token_expires
    lib_admin_crud.save_token(db=db, token=access_token, token_type="bearer", expires_at=expires_at)
    lib_admin_crud.create_lib_admin(db=db, lib_admin=lib_admin, access_token=access_token)
    return LibAdminBaseToken(email = lib_admin.email, token = access_token)


# Log in the library admin and issue a JWT access token
@router.post("/lib_admin/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"Attempting to log in with: {form_data.username}, {form_data.password}")
    admin = authenticate_admin(db, email=form_data.username, password=form_data.password)
    if not admin:
        print("Authentication failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print("Authentication successful")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email},
        db=db,
        token_type="bearer",
        expires_delta=access_token_expires
    )

    expires_at = datetime.utcnow() + access_token_expires
    lib_admin_crud.save_token(db=db, token=access_token, token_type="bearer", expires_at=expires_at)

    return Token(access_token=access_token, token_type="bearer")

