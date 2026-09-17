from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from database import Base

class user(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(50), unique = True, nullable = True)
    email = Column(String, unique = True, index = True,nullable = True)
    hashed_password = Column(String, nullable = True)
    created_at = Column(DateTime, server_default = func.now())
    
