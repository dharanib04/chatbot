import asyncio
from .config import load_settings
from .core import Chatbot
from .tools.registry import ToolRegistry
from .tools.calculator import CalculatorTool
from .tools.weather import WeatherTool
from .tools.file_system import FileSystemTool
from . import ui

async def amain():
    """The main asynchronous function that runs the chatbot CLI."""
    try:
        settings = load_settings()
    except ValueError as e:
        ui.print_error(str(e))
        return

    # Set up the tool registry
    tool_registry = ToolRegistry()
    tool_registry.register(CalculatorTool())
    tool_registry.register(WeatherTool())
    tool_registry.register(FileSystemTool())

    # Initialize the chatbot
    chatbot = Chatbot(settings, tool_registry)
    ui.print_welcome_message()

    while True:
        try:
            user_input = ui.console.input("[bold cyan]>>> [/bold cyan]")
            
            if user_input.lower() in ["quit", "exit"]:
                break
            if user_input.lower() in ["help", "tools"]:
                ui.print_help(tool_registry)
                continue
            if user_input.lower() == "clear":
                chatbot.clear_history()
                ui.console.print("[green]Conversation history cleared.[/green]")
                continue

            # No need for a separate UI print here, the core logic handles it
            final_response = await chatbot.run_chat_turn(user_input)
            ui.print_assistant_response(final_response)

        except KeyboardInterrupt:
            break
        except Exception as e:
            ui.print_error(f"An unexpected error occurred: {e}")
    
    ui.console.print("[bold blue]Goodbye![/bold blue]")

def cli():
    """Synchronous wrapper for the async main function."""
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        ui.console.print("\n[bold blue]Goodbye![/bold blue]")

if __name__ == "__main__":
    cli()