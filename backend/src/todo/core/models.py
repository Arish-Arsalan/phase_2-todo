from pydantic import BaseModel
from typing import Dict, List, Optional
from enum import Enum
import uuid
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    tags: List[str] = []
    due_date: Optional[datetime] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    meta: Dict = {}

class SkillResponse(BaseModel):
    success: bool
    message: str
     Optional[Dict] = None
