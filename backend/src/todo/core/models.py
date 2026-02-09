from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    meta: dict = {}
