# app/main.py
from fastapi import FastAPI
from routes import ops, client
from database.database import engine
from models.models import Base

# Create all tables (if not using Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(ops.router, prefix="/ops", tags=["Operations User"])
app.include_router(client.router, prefix="/client", tags=["Client User"])