from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .schemas import Task, TaskCreate, TaskUpdate, DashboardStats, SkillInfo
from ..core.orchestrator import AIOrchestrator
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["todo"])

# Global orchestrator instance
orchestrator = AIOrchestrator()

@router.get("/health", summary="Health check")
async def health_check():
    return {"status": "healthy", "timestamp": "2026-02-10"}

@router.get("/dashboard/stats", response_model=DashboardStats, summary="Get dashboard statistics")
async def get_dashboard_stats():
    stats = orchestrator.get_stats()
    return DashboardStats(
        total_tasks=sum(stats.values()),
        completed_tasks=stats.get('emails_sent', 0) + stats.get('linkedin_posts', 0) + stats.get('telegram_messages', 0) + stats.get('general_tasks', 0),
        pending_tasks=0,  # Would come from queue
        success_rate=95.0,  # Calculate based on success/failure ratio
        skills_loaded=stats.get('skills_loaded', 0),
        emails_sent=stats.get('emails_sent', 0),
        linkedin_posts=stats.get('linkedin_posts', 0),
        telegram_messages=stats.get('telegram_messages', 0)
    )

@router.get("/skills", response_model=List[SkillInfo], summary="List available skills")
async def list_skills():
    skills_info = []
    for name, skill in orchestrator.skills.items():
        skills_info.append(SkillInfo(
            name=name,
            loaded=True,
            description=getattr(skill, '__doc__', 'No description available')
        ))
    return skills_info

@router.post("/tasks", response_model=Task, summary="Create a new task")
async def create_task(task: TaskCreate):
    # Convert to internal Task model and process
    internal_task = Task(
        id=uuid.uuid4().int % 1000000,  # Simple ID generation
        user_id="default_user",
        title=task.title,
        description=task.description,
        status=task.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Execute the task
    result = orchestrator.execute_task(internal_task)
    
    return Task(
        id=internal_task.id,
        user_id=internal_task.user_id,
        title=internal_task.title,
        description=internal_task.description,
        status=internal_task.status,
        created_at=internal_task.created_at,
        updated_at=internal_task.updated_at
    )

@router.get("/tasks", response_model=List[Task], summary="List all tasks")
async def list_tasks():
    # Return mock tasks since we're using file-based storage
    return [
        Task(
            id=1,
            user_id="default_user",
            title="Sample Task",
            description="This is a sample task",
            status=TaskStatus.COMPLETED,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]

@router.get("/tasks/{task_id}", response_model=Task, summary="Get task by ID")
async def get_task(task_id: int):
    # Return mock task
    return Task(
        id=task_id,
        user_id="default_user",
        title=f"Task {task_id}",
        description=f"Description for task {task_id}",
        status=TaskStatus.IN_PROGRESS,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@router.put("/tasks/{task_id}", response_model=Task, summary="Update a task")
async def update_task(task_id: int, task_update: TaskUpdate):
    # Mock update
    return Task(
        id=task_id,
        user_id="default_user",
        title=task_update.title or f"Task {task_id}",
        description=task_update.description or f"Description for task {task_id}",
        status=task_update.status or TaskStatus.PENDING,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@router.delete("/tasks/{task_id}", summary="Delete a task")
async def delete_task(task_id: int):
    # Mock deletion
    return {"message": f"Task {task_id} deleted"}
