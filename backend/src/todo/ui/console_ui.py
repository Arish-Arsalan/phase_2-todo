import time
import os
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
import threading

console = Console()

class ConsoleUI:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.running = True
        self.spinner = Spinner("clock")
    
    def create_status_table(self):
        """Create status table with current statistics"""
        table = Table(title="Todo System Status")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        
        stats = self.orchestrator.get_stats()
        
        table.add_row("Skills Loaded", str(stats.get('skills_loaded', 0)))
        table.add_row("Emails Sent", str(stats.get('emails_sent', 0)))
        table.add_row("LinkedIn Posts", str(stats.get('linkedin_posts', 0)))
        table.add_row("Telegram Messages", str(stats.get('telegram_messages', 0)))
        table.add_row("General Tasks", str(stats.get('general_tasks', 0)))
        table.add_row("Tasks Failed", str(stats.get('tasks_failed', 0)))
        
        return table
    
    def create_progress_bars(self):
        """Create progress bars for ongoing activities"""
        progress_table = Table(title="System Activity")
        progress_table.add_column("Activity", style="cyan")
        progress_table.add_column("Progress", style="magenta")
        
        stats = self.orchestrator.get_stats()
        total_completed = sum([
            stats.get('emails_sent', 0),
            stats.get('linkedin_posts', 0),
            stats.get('telegram_messages', 0),
            stats.get('general_tasks', 0)
        ])
        
        progress_table.add_row("Overall Processing", f"{total_completed} tasks completed")
        
        return progress_table
    
    def render_layout(self):
        """Render the main layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["header"].update(
            Panel("[bold blue]í´– TODO SYSTEM[/bold blue]", style="white on blue")
        )
        
        layout["main"].split_row(
            Layout(name="status"),
            Layout(name="activity")
        )
        
        layout["status"].update(Panel(self.create_status_table(), title="System Stats"))
        layout["activity"].update(Panel(self.create_progress_bars(), title="Activity"))
        
        layout["footer"].update(
            Panel(f"[green]Status:[/green] Running | [yellow]Time:[/yellow] {time.strftime('%H:%M:%S')}", 
                  style="white on green")
        )
        
        return layout
    
    def run(self):
        """Run the console UI"""
        with Live(self.render_layout(), refresh_per_second=4, console=console) as live:
            while self.running:
                try:
                    live.update(self.render_layout())
                    time.sleep(1)
                except KeyboardInterrupt:
                    self.running = False
                    break
