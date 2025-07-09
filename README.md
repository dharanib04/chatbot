# Project I: AI-Powered CLI Assistant

This is a modular command-line AI assistant that integrates with OpenAI's GPT-4o-mini model, featuring an extensible tool system for function calling.

## Features

- **Modern Project Management**: Uses `uv` for dependency and environment management.
- **Extensible Tools**: Easily add new tools by implementing a simple `Tool` protocol.
- **Function Calling**: Integrates with OpenAI's function calling API.
- **Async Architecture**: Uses `asyncio` for non-blocking API calls and concurrent tool execution.
- **Rich CLI**: Beautiful and clear terminal interface using the `rich` library.
- **Secure Configuration**: Manages API keys via `.env` files.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd chatbot-cli
    ```

2.  **Create a virtual environment and install dependencies using `uv`:**
    ```bash
    # Create the virtual environment
    uv venv

    # Activate the environment
    # On macOS/Linux
    source .venv/bin/activate
    # On Windows
    .venv\Scripts\activate

    # Install dependencies
    uv pip install -e .
    ```
    *The `-e .` flag installs the project in "editable" mode, so changes to the source code are immediately reflected.*

## Configuration

1.  **Create a `.env` file** by copying the example template:
    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file** and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-..."
    ```

## Usage

Run the chatbot from your terminal:

```bash
chatbot