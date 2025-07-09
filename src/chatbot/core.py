import asyncio
import json
from typing import cast
from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageParam,
)

from .config import Settings
from .tools.registry import ToolRegistry
from . import ui

class Chatbot:
    """
    The core chatbot class that manages the conversation,
    interfaces with the OpenAI API, and handles tool execution.
    """
    def __init__(self, settings: Settings, tool_registry: ToolRegistry):
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.tool_registry = tool_registry
        self.history: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "You are a helpful command-line assistant. "
                           "Be concise and use the available tools when necessary.",
            }
        ]


    async def run_chat_turn(self, user_input: str) -> str:
        """
        Manages a single turn of the conversation, including potential tool calls.
        """
        self.history.append({"role": "user", "content": user_input})
        
        while True:
            # The type errors on 'messages' and 'tools' are now resolved by the
            # more specific type hints used in this class and the ToolRegistry.
            response = await self.client.chat.completions.create(
                model=self.settings.model,
                messages=self.history,
                tools=self.tool_registry.get_all_schemas(),
                tool_choice="auto",
                temperature=self.settings.temperature,
            )
            response_message = response.choices[0].message
            message_to_append = cast(
                ChatCompletionMessageParam, 
                response_message.model_dump(exclude_none=True)
            )
            self.history.append(message_to_append)


            if not response_message.tool_calls:
                # No tool calls, the turn is over.
                return response_message.content or ""

            # The model wants to call one or more tools.
            await self._handle_tool_calls(response_message)
            # Loop again to get the final response from the model.

    async def _handle_tool_calls(self, response_message: ChatCompletionMessage):
        """
        Executes tool calls requested by the model, concurrently.
        """
        tool_calls = response_message.tool_calls
        
        # --- CHANGE 4: Add a guard clause to handle when tool_calls is None ---
        if not tool_calls:
            return

        # Use asyncio.gather to execute all tool calls in parallel.
        tool_tasks = []
        for tool_call in tool_calls:
            tool_tasks.append(self._execute_single_tool(tool_call))
            
        tool_results = await asyncio.gather(*tool_tasks)

        # Append all tool results to the conversation history.
        for result in tool_results:
            self.history.append(result)

    async def _execute_single_tool(self, tool_call) -> dict:
        """Executes a single tool and returns the result message for history."""
        tool_name = tool_call.function.name
        tool = self.tool_registry.get_tool(tool_name)
        
        try:
            arguments = json.loads(tool_call.function.arguments)
            ui.print_tool_call(tool_name, arguments)

            if not tool:
                result = f"Error: Tool '{tool_name}' not found."
            else:
                result = await tool.execute(**arguments)

        except json.JSONDecodeError:
            result = f"Error: Invalid arguments format for {tool_name}."
        except Exception as e:
            result = f"Error executing tool {tool_name}: {e}"

        ui.print_tool_result(result)
        
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": result,
        }
        
    def clear_history(self):
        """Clears the conversation history, keeping only the system prompt."""
        self.history = self.history[:1]