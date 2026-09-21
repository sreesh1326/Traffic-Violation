from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from auth.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer
from detection.model import run_detection
from datetime import datetime

router = APIRouter(prefix="/detection", tags=["Detection"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/Login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    return email

@router.post("/detect")
async def analyze_image(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("/image"):
        raise HTTPException(status_code=400, detail="File must be an integer")

    image_bytes = await file.read()
    violations, annotated_image = run_detection(image_bytes)
    
    return {
        "violations": violations,
        "annotated_image": annotated_image,
        "timestamp": datetime.utcnow(),
        "analyzed_by": current_user
    }