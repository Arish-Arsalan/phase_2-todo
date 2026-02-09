<<<<<<< HEAD
ï»¿#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Todo System - Phase 1: Console Application
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def main():
    print("ðŸ¤– Todo System - Phase 1")
    print("=" * 50)
    print("Console application with rich UI and agent skills")
    print("âœ… Ready to run")

if __name__ == "__main__":
    main()
=======
#!/usr/bin/env python3
"""
Todo System - Phase 1: Console Application with Rich UI
"""

import sys
import time
from pathlib import Path
import threading
from .src.todo.core.orchestrator import AIOrchestrator
from .src.todo.ui.console_ui import ConsoleUI

def main():
    print("í´– TODO SYSTEM - PHASE 1")
    print("=" * 50)
    print("Initializing Console Application with Rich UI")
    
    # Initialize orchestrator
    orchestrator = AIOrchestrator()
    
    # Start console UI in background thread
    ui = ConsoleUI(orchestrator)
    ui_thread = threading.Thread(target=ui.run, daemon=True)
    ui_thread.start()
    
    print("âœ… Console UI started")
    print("âœ… System operational")
    print("âœ… Press Ctrl+C to stop")
    
    try:
        # Main processing loop
        while True:
            # This is where the Ralph Wiggum loop would run
            # For now, just keep the system alive
            time.sleep(5)
    except KeyboardInterrupt:
        print("\ní»‘ Shutting down Todo System...")
        ui.running = False
        ui_thread.join(timeout=2)
        print("âœ… System shutdown complete")

if __name__ == "__main__":
    main()
>>>>>>> f11395e3f7cee67d944479136e98ac1bddb0be36
