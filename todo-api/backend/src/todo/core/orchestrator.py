from typing import Dict, Any
from .models import Task, TaskStatus
import importlib
import os
from pathlib import Path
import time
import threading
from collections import defaultdict

class AIOrchestrator:
    def __init__(self):
        self.skills = {}
        self.stats = defaultdict(int)
        self.lock = threading.Lock()
        self.load_skills()
    
    def load_skills(self):
        """Load all available skills"""
        skills_dir = Path(__file__).parent.parent / "skills"
        for skill_file in skills_dir.glob("*.py"):
            if skill_file.name != "__init__.py":
                skill_name = skill_file.stem
                try:
                    spec = importlib.util.spec_from_file_location(
                        skill_name, skill_file
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.skills[skill_name] = module
                    print(f"✅ Loaded skill: {skill_name}")
                    self.stats['skills_loaded'] += 1
                except Exception as e:
                    print(f"❌ Failed to load skill {skill_name}: {e}")
    
    def execute_task(self, task: Task) -> Dict[str, Any]:
        """Execute a task using appropriate skill"""
        try:
            # Determine which skill to use based on task type
            if "email" in task.title.lower():
                return self.execute_email_task(task)
            elif "linkedin" in task.title.lower():
                return self.execute_linkedin_task(task)
            elif "telegram" in task.title.lower():
                return self.execute_telegram_task(task)
            else:
                return self.execute_general_task(task)
        except Exception as e:
            self.stats['tasks_failed'] += 1
            return {"success": False, "message": f"Task failed: {str(e)}"}
    
    def execute_email_task(self, task: Task) -> Dict[str, Any]:
        if 'email_sender' in self.skills:
            try:
                result = self.skills['email_sender'].send_email(
                    task.meta.get('to', ''),
                    task.meta.get('subject', ''),
                    task.meta.get('body', '')
                )
                self.stats['emails_sent'] += 1
                return result
            except Exception as e:
                return {"success": False, "message": f"Email failed: {str(e)}"}
        return {"success": False, "message": "Email skill not available"}
    
    def execute_linkedin_task(self, task: Task) -> Dict[str, Any]:
        if 'linkedin_publisher' in self.skills:
            try:
                result = self.skills['linkedin_publisher'].publish_post(
                    task.description,
                    task.meta.get('hashtags', [])
                )
                self.stats['linkedin_posts'] += 1
                return result
            except Exception as e:
                return {"success": False, "message": f"LinkedIn failed: {str(e)}"}
        return {"success": False, "message": "LinkedIn skill not available"}
    
    def execute_telegram_task(self, task: Task) -> Dict[str, Any]:
        if 'telegram_sender' in self.skills:
            try:
                result = self.skills['telegram_sender'].send_telegram_message(
                    task.meta.get('chat_id', ''),
                    task.description
                )
                self.stats['telegram_messages'] += 1
                return result
            except Exception as e:
                return {"success": False, "message": f"Telegram failed: {str(e)}"}
        return {"success": False, "message": "Telegram skill not available"}
    
    def execute_general_task(self, task: Task) -> Dict[str, Any]:
        # Use file processor for general tasks
        if 'file_processor' in self.skills:
            try:
                result = self.skills['file_processor'].process_needs_action(self)
                self.stats['general_tasks'] += 1
                return result
            except Exception as e:
                return {"success": False, "message": f"General task failed: {str(e)}"}
        return {"success": False, "message": "General skill not available"}
    
    def get_stats(self) -> Dict[str, int]:
        """Get current system statistics"""
        with self.lock:
            return dict(self.stats)
