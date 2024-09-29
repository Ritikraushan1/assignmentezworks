# app/routes/ops.py
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from schemas.schemas import FileSchema, Token
from auth.auth import authenticate_user, create_access_token, get_current_ops_user
from crud.crud import create_file
from models.models import File
from config import settings
from database.database import SessionLocal
from datetime import timedelta

router = APIRouter()

@router.post("/login", response_model=Token)
def ops_login(form_data: Depends(), db: Session = Depends(SessionLocal)):
    # Implement login logic here
    pass  # Placeholder

@router.post("/upload", response_model=FileSchema)
async def upload_file(
    file: UploadFile = File(...), 
    current_user: File = Depends(get_current_ops_user),
    db: Session = Depends(SessionLocal)
):
    allowed_extensions = ["pptx", "docx", "xlsx"]
    extension = file.filename.split(".")[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    upload_dir = os.path.join(os.getcwd(), "uploaded_files")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    db_file = create_file(db, filename=file.filename, filepath=file_path, owner_id=current_user.id)
    return db_file
