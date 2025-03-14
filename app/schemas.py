from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# Schema for creating a task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority


# Schema for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


# Schema for reading a task
class Task(TaskCreate):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# schema to create the user
class CreateUser(BaseModel):
    email: EmailStr
    password: str
    username: str


# schema to read the user
class User(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None