# app/routes/client.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from  schemas.schemas import UserCreate, Token, FileSchema
from  auth.auth import authenticate_user, create_access_token, get_current_active_user
from  crud.crud import get_user_by_email, create_user, get_all_files, get_file_by_id
from  models.models import User, File
from  config import settings
from  database.database import SessionLocal
from datetime import timedelta
from utils.email import generate_verification_url, send_verification_email

router = APIRouter()

@router.post("/signup", response_model=Token)
def client_signup(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user)
    
    verification_url = generate_verification_url(new_user)
    send_verification_email(new_user.email, verification_url)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(SessionLocal)):
    # Implement email verification logic
    pass  # Placeholder

@router.post("/login", response_model=Token)
def client_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user or user.is_ops:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials or not a Client User",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Email not verified")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_ops": user.is_ops}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/files", response_model=List[FileSchema])
def list_files(current_user: User = Depends(get_current_active_user), db: Session = Depends(SessionLocal)):
    files = get_all_files(db)
    return files

@router.get("/download/{file_id}")
def download_file(file_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(SessionLocal)):
    file = get_file_by_id(db, file_id=file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file.filepath, filename=file.filename)
