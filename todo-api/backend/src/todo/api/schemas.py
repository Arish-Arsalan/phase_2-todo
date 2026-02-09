from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskBase(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class Task(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(BaseModel):
    id: str
    email: str
    created_at: datetime

class DashboardStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    success_rate: float
    skills_loaded: int
    emails_sent: int
    linkedin_posts: int
    telegram_messages: int

class SkillInfo(BaseModel):
    name: str
    loaded: bool
    description: str
