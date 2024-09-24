
from datetime import datetime
from pydantic import BaseModel, EmailStr

class LibAdminBase(BaseModel):
    email : EmailStr
    password : str

class LibAdminTokenBase(BaseModel):
    access_token: str
    token_type: str
    expires_at : datetime   

class Token(BaseModel):
    access_token: str
    token_type: str