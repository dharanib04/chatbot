import os
from typing import Any, Dict
from .base import Tool

class FileSystemTool(Tool):
    """A tool to list files in a directory."""
    name = "list_files"
    description = "Lists all files and directories in a specified path."

    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The directory path to list. Defaults to the current directory.",
                        },
                    },
                    "required": [],
                },
            },
        }

    async def execute(self, path: str = ".") -> str:
        """
        Lists files in the given directory path.
        Includes error handling for non-existent paths.
        """
        try:
            files = os.listdir(path)
            if not files:
                return f"The directory '{path}' is empty."
            return f"Files in '{path}':\n- " + "\n- ".join(files)
        except FileNotFoundError:
            return f"Error: The directory '{path}' does not exist."
        except Exception as e:
            return f"An unexpected error occurred: {e}"