from pydantic import BaseModel
<<<<<<< HEAD
from typing import List, Optional
=======
from typing import Dict, List, Optional
>>>>>>> f11395e3f7cee67d944479136e98ac1bddb0be36
from enum import Enum
import uuid
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    COMPLETED = "completed"
    FAILED = "failed"

<<<<<<< HEAD
=======
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

>>>>>>> f11395e3f7cee67d944479136e98ac1bddb0be36
class Task(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
<<<<<<< HEAD
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    meta: dict = {}
=======
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
>>>>>>> f11395e3f7cee67d944479136e98ac1bddb0be36
