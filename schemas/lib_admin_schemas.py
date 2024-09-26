
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, validator

class LibAdminBaseToken(BaseModel):
    email: EmailStr
    token: str  

class LibAdminBasePassword(BaseModel):
    email : EmailStr
    password : constr(min_length=8, max_length=32) 

    @validator('password')
    def validate_password_strength(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one number')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        return value
    
class LibAdminTokenBase(BaseModel):
    access_token: str
    token_type: str
    expires_at : datetime   

class Token(BaseModel):
    access_token: str
    token_type: str