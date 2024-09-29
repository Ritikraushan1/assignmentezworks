# app/utils/file_handler.py
import os
import shutil
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {"pptx", "docx", "xlsx"}

def save_upload_file(upload_file: UploadFile, destination: str):
    extension = upload_file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
