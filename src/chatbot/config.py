import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    """
    Configuration class to store application settings.
    Uses a dataclass for type safety and immutability.
    """
    openai_api_key: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.7

def load_settings() -> Settings:
    """
    Loads settings from environment variables.
    Validates that required variables are set.
    """
    load_dotenv()  # Load .env file

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable not found. "
            "Please create a .env file and add your key."
        )

    return Settings(
        openai_api_key=api_key,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", 0.7)),
    )