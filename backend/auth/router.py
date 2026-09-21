from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import models, schemas
from auth.jwt import create_access_token
from passlib.context import CryptContext

router = APIRouter(prefix = "/auth", tags = ["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

@router.post("/register", response_model = schemas.userResponse)
def register(user: schemas.userRegistration, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Email already existed lil bro")
    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(username = user.username,
                           email = user.email,
                           hashed_password = hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model = schemas.TokenResponse)
def login(user: schemas.userLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Invalid credentials")
    access_token = create_access_token(data = {"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
        

        