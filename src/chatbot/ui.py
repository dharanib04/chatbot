from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text

# Create a single console object to manage all terminal output
console = Console()

def print_welcome_message():
    """Prints a styled welcome message."""
    welcome_text = Text.from_markup(
        "[bold blue]🤖 AI-Powered CLI Assistant[/bold blue]\n\n"
        "Connected to OpenAI with tool support!\n"
        "Type your message, or use special commands:\n"
        "[cyan]help, tools, clear, exit, quit[/cyan]"
    )
    panel = Panel(
        welcome_text,
        title="[bold green]Welcome[/bold green]",
        border_style="green",
        padding=(1, 2)
    )
    console.print(panel)

def print_user_prompt(text: str):
    """Prints the user's message in a styled panel."""
    panel = Panel(text, title="[bold blue]You[/bold blue]", border_style="blue")
    console.print(panel)

def print_assistant_response(text: str):
    """Prints the assistant's response, rendering Markdown."""
    panel = Panel(Markdown(text), title="[bold green]Assistant[/bold green]", border_style="green")
    console.print(panel)

def print_tool_call(tool_name: str, args: dict):
    """Prints a table visualizing a tool call."""
    table = Table(title=f"🔧 Calling Tool: [bold cyan]{tool_name}[/bold cyan]")
    table.add_column("Parameter", style="magenta")
    table.add_column("Value", style="yellow")
    for key, value in args.items():
        table.add_row(key, str(value))
    console.print(table)

def print_tool_result(result: str):
    """Prints the result of a tool execution in a panel."""
    panel = Panel(f"[bright_black]{result}[/bright_black]", title="[bold yellow]Tool Result[/bold yellow]", border_style="yellow")
    console.print(panel)

def print_error(message: str):
    """Prints an error message in a styled panel."""
    panel = Panel(f"[bold red]{message}[/bold red]", title="[bold red]Error[/bold red]", border_style="red")
    console.print(panel)

def print_help(tool_registry):
    """Prints a help message listing available tools."""
    table = Table(title="Available Tools")
    table.add_column("Tool Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="green")

    for tool in tool_registry.get_all_tools():
        table.add_row(tool.name, tool.description)

    console.print(table)