"""
Skill: File Processor
Handles file-based task processing for the AI Todo system
"""

import json
import time
from pathlib import Path
from datetime import datetime

def process_needs_action(agent):
    """Process files in the Needs Action folder"""
    vault_path = agent.vault_path
    needs_action_folder = vault_path / 'Vault' / 'Needs_Action'
    
    # Create the folder if it doesn't exist
    needs_action_folder.mkdir(exist_ok=True)
    
    # Get all markdown files in Needs Action
    files = list(needs_action_folder.glob('*.md'))
    
    processed_count = 0
    for file_path in files:
        try:
            # Read the file content
            content = file_path.read_text(encoding='utf-8')
            
            # Create a task based on file content
            task_title = f"Process: {file_path.stem}"
            task_description = content[:200] + "..." if len(content) > 200 else content
            
            # Move to Pending Approval
            pending_approval_folder = vault_path / 'Vault' / 'Pending_Approval'
            pending_approval_folder.mkdir(exist_ok=True)
            
            # Create approval file
            approval_file = pending_approval_folder / f"APPROVE_{file_path.stem}_{int(time.time())}.md"
            approval_file.write_text(f"# Approval Request\n\nTitle: {task_title}\n\nDescription: {task_description}\n\nStatus: PENDING\n")
            
            # Archive the original file
            archive_folder = needs_action_folder / 'archive'
            archive_folder.mkdir(exist_ok=True)
            file_path.rename(archive_folder / file_path.name)
            
            processed_count += 1
            print(f"✅ Processed: {task_title}")
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
    
    return {"success": True, "processed": processed_count}
