# Phase 1: Console Application with Rich UI

## Objective
Implement a self-contained console-based AI Todo agent using Agent Skills architecture.

## Requirements
- [ ] Agent Skills: modular pluggable skills (file_processor, approval_manager, etc.)
- [ ] Ralph Wiggum autonomous loop (self-running task processor)
- [ ] Rich terminal UI with `rich` (progress bars, tables, colors)
- [ ] File-based vault system (Inbox → Needs Action → Pending Approval → Done)
- [ ] Dashboard showing real-time stats (tasks processed, success rate, skills loaded)

## Success Criteria
- Runs `python backend/main.py` → shows live dashboard
- Processes 100+ tasks automatically via Ralph Wiggum loop
- Skills load dynamically from `skills/` directory
- No external dependencies except Python 3.13 + pip packages
