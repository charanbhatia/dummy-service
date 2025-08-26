from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"


class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    created_at: datetime


class MessageResponse(BaseModel):
    message: str
    timestamp: datetime
    data: Optional[dict] = None
