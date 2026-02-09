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
        skills_dir = Path(__file__).parent.parent / "skills"
        for skill_file in skills_dir.glob("*.py"):
            if skill_file.name != "__init__.py":
                skill_name = skill_file.stem
                try:
                    spec = importlib.util.spec_from_file_location(skill_name, skill_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.skills[skill_name] = module
                    print(f"✅ Loaded skill: {skill_name}")
                    self.stats['skills_loaded'] += 1
                except Exception as e:
                    print(f"❌ Failed to load {skill_name}: {e}")

    def execute_task(self, task: Task) -> Dict[str, Any]:
        # Placeholder — will be implemented by Claude Code after spec
        return {"success": True, "message": f"Task '{task.title}' processed"}
    
    def get_stats(self) -> Dict[str, int]:
        with self.lock:
            return dict(self.stats)
