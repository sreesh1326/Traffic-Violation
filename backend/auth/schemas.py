from pydantic import BaseModel, EmailStr
from datetime import datetime

class userRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str

class userLogin(BaseModel):
    email: EmailStr
    password: str

class userResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    