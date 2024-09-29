# app/crud/crud.py
from sqlalchemy.orm import Session
from models.models import User, File
from schemas.schemas import UserCreate
from auth.auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_ops=user.is_ops
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_files(db: Session):
    return db.query(File).all()

def get_file_by_id(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()

def create_file(db: Session, filename: str, filepath: str, owner_id: int):
    db_file = File(filename=filename, filepath=filepath, owner_id=owner_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
