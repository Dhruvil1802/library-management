from sqlalchemy import Column, Integer, String, DateTime
from database import Base  
from datetime import datetime



class LibAdmin(Base):
    __tablename__ = "lib_admin"


    lib_admin_id = Column(Integer, primary_key=True, index=True)

    email = Column(String(length=255), unique=True, index=True) 

    password = Column(String(length=255))  




class LibAdminToken(Base):
    __tablename__ = "lib_admin_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(256), unique=True, nullable=False)
    token_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
