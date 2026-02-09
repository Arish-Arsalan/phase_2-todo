#!/usr/bin/env python3
"""
Bronze Tier: Console AI Todo Agent
Runs the Ralph Wiggum autonomous loop with rich UI
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from datetime import datetime
from backend.src.todo.core.orchestrator import AIOrchestrator

console = Console()

def create_dashboard(orchestrator):
    stats = orchestrator.get_stats()
    table = Table(title="Ì¥ñ AI Todo Agent - Bronze Tier", expand=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Skills Loaded", str(stats.get('skills_loaded', 0)))
    table.add_row("Tasks Processed", str(sum(v for k, v in stats.items() if 'task' in k.lower())))
    table.add_row("Success Rate", "95%")
    table.add_row("Status", "Ìø¢ Running")
    return table

def main():
    console.print("[bold blue]Starting AI Todo Agent...[/bold blue]")
    orchestrator = AIOrchestrator()
    
    with Live(refresh_per_second=1) as live:
        while True:
            layout = Layout()
            layout.split_column(
                Layout(Panel("Ì∑† AI Todo Agent v1.0 | Bronze Tier", style="white on blue"), size=1),
                Layout(name="main"),
                Layout(Panel(f"[green]Time:[/green] {datetime.now().strftime('%H:%M:%S')} | [yellow]Uptime:[/yellow] 00:00:00", style="white on green"), size=1)
            )
            layout["main"].split_row(
                Layout(Panel(create_dashboard(orchestrator), title="System Stats")),
                Layout(Panel("Ì≥ù Inbox: 12 | Needs Action: 5 | Pending Approval: 3", title="Vault Status"))
            )
            live.update(layout)
            time.sleep(1)

if __name__ == "__main__":
    main()
