# app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/securefilesharing")
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.yourprovider.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "your_smtp_username")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "your_smtp_password")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@yourdomain.com")

    class Config:
        env_file = ".env"

settings = Settings()
