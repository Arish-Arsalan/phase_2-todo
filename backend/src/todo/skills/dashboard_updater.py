"""
Skill: Dashboard Updater
Updates the dashboard with current system status
"""

import json
import time
from pathlib import Path
from datetime import datetime

def update_dashboard(agent):
    """Update the dashboard with current system status"""
    vault_path = agent.vault_path
    dashboard_file = vault_path / 'Vault' / 'Dashboard.md'
    
    # Get vault folder paths
    folders = agent.get_vault_folders()
    
    # Count files in each folder
    stats = {}
    for folder_name, folder_path in folders.items():
        if folder_path.exists():
            stats[folder_name] = len(list(folder_path.glob('*')))
        else:
            stats[folder_name] = 0
    
    # Create dashboard content
    dashboard_content = f"""# Ì≥ä AI Todo System Dashboard

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Ì≥à System Statistics

| Folder | Count | Status |
|--------|-------|--------|
| Inbox | {stats.get('inbox', 0)} | Ì≥• |
| Needs Action | {stats.get('needs_action', 0)} | ‚ö†Ô∏è |
| Pending Approval | {stats.get('pending_approval', 0)} | Ì¥Ñ |
| Approved | {stats.get('approved', 0)} | ‚úÖ |
| Done | {stats.get('done', 0)} | Ìæâ |
| Plans | {stats.get('plans', 0)} | Ì≥ã |

## Ì≥ä Overall Status
- Total Tasks: {sum(stats.values())}
- System Health: Excellent
- Last Processed: {datetime.now().strftime('%H:%M:%S')}

## Ì∫Ä Agent Status
- Skills Loaded: {len(getattr(agent, 'skills', {}))}
- Processing Mode: Active
- Version: 1.0.0

*Generated automatically by AI Todo System*
"""
    
    # Write dashboard
    dashboard_file.write_text(dashboard_content)
    
    print(f"Ì≥ä Dashboard updated: {dashboard_file.name}")
    return {"success": True, "updated": dashboard_file.name}
