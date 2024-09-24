from datetime import datetime
from pydantic import BaseModel, EmailStr

class StudentBase(BaseModel):
    email : EmailStr
    password : str 
    name : str 

class StudentTokenBase(BaseModel):
    access_token: str
    token_type: str
    expires_at : datetime

class Token(BaseModel):
    access_token: str
    token_type: str