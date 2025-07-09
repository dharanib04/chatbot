from typing import Any, Dict
from .base import Tool

class WeatherTool(Tool):
    """A tool to get the current weather for a given location."""
    name = "get_weather"
    description = "Provides the current weather for a specified city."

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g., 'San Francisco'.",
                        },
                    },
                    "required": ["location"],
                },
            },
        }

    async def execute(self, location: str) -> str:
        """
        Returns a mock weather report. In a real application, this would
        call a weather API.
        """
        return f"The weather in {location} is currently sunny and 25°C (77°F)."