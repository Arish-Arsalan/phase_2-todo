"""
Skill: Approval Manager
Handles approval workflow for the AI Todo system
"""

import json
import time
from pathlib import Path
from datetime import datetime

def process_approved_files(agent):
    """Process approved files and move them to Done"""
    vault_path = agent.vault_path
    pending_approval_folder = vault_path / 'Vault' / 'Pending_Approval'
    approved_folder = vault_path / 'Vault' / 'Approved'
    done_folder = vault_path / 'Vault' / 'Done'
    
    # Create folders if they don't exist
    pending_approval_folder.mkdir(exist_ok=True)
    approved_folder.mkdir(exist_ok=True)
    done_folder.mkdir(exist_ok=True)
    
    # Get all approved files
    approved_files = list(approved_folder.glob('*.md'))
    
    processed_count = 0
    for file_path in approved_files:
        try:
            # Read the file content
            content = file_path.read_text(encoding='utf-8')
            
            # Move to Done
            done_file = done_folder / f"DONE_{file_path.stem}_{int(time.time())}.md"
            done_file.write_text(content + f"\n\nStatus: COMPLETED\nCompleted: {datetime.now()}\n")
            
            # Archive the original file
            archive_folder = approved_folder / 'archive'
            archive_folder.mkdir(exist_ok=True)
            file_path.rename(archive_folder / file_path.name)
            
            processed_count += 1
            print(f"✅ Completed: {file_path.stem}")
            
        except Exception as e:
            print(f"❌ Error completing {file_path}: {e}")
    
    return {"success": True, "completed": processed_count}
