from typing import Protocol, Any, Dict

class Tool(Protocol):
    """
    A protocol defining the contract for any tool that can be used by the chatbot.
    This encourages duck typing while providing static type checking.
    """
    name: str
    description: str

    def get_schema(self) -> Dict[str, Any]:
        """Returns the JSON schema for the tool, required by OpenAI."""
        ...

    async def execute(self, **kwargs) -> str:
        """
        Executes the tool's logic with the given arguments.
        This is an async function to support non-blocking I/O.
        """
        ...