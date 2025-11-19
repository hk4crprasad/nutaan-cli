# Nutaan CLI Project Documentation

## 1. Project Overview

**Nutaan-CLI** is a powerful ReAct (Reasoning and Acting) Python assistant designed for the terminal. It leverages Large Language Models (LLMs) to perform complex tasks, manage plans, and interact with the system.

### Key Features
- **AI-Powered Assistant**: Uses LangGraph and LangChain for advanced reasoning.
- **Think Mode**: A dedicated mode for complex problem analysis and reasoning.
- **Plan Management**: Persistent todo lists with progress tracking and strikethrough formatting.
- **Multi-Model Support**: Compatible with OpenAI, Anthropic, Google Gemini, Mistral, and more.
- **Rich Terminal UI**: Beautiful output with syntax highlighting, progress bars, and formatted tables.
- **Tool Ecosystem**: Includes tools for web search, file operations, bash commands, and more.

## 2. Project Structure

```
nutaan-cli/
├── nutaan/                      # Source code package
│   ├── __init__.py
│   ├── __main__.py              # Module entry point
│   ├── cli.py                   # CLI entry point and UI logic
│   ├── core/                    # Core logic
│   │   ├── agent_manager.py     # Agent creation and management
│   │   ├── llm_manager.py       # LLM provider configuration
│   │   ├── prompt_system.py     # System prompts
│   │   ├── session_history.py   # Session persistence
│   │   ├── config_manager.py    # Configuration handling
│   │   └── tool_approval_manager.py # Human-in-the-loop approval
│   └── tools/                   # Tool implementations
│       ├── plan_tool.py         # Plan/Todo management
│       ├── think_tool.py        # Reasoning tool
│       ├── brave_search_tool.py # Web search
│       ├── bash_run_tool.py     # System commands
│       ├── file_read_tool.py    # File reading
│       ├── file_write_tool.py   # File writing
│       └── file_edit_tool.py    # File editing
├── .nutaan_data/                # Persistent data storage (plans, etc.)
├── tests/                       # Test suite
├── pyproject.toml               # Project configuration and dependencies
├── requirements.txt             # Python dependencies
├── README.md                    # User documentation
└── LICENSE                      # MIT License
```

## 3. Installation & Setup

### Prerequisites
- Python 3.8 or higher
- API keys for LLM providers (OpenAI, Anthropic, etc.)

### Installation
```bash
# From PyPI
pip install nutaan-cli

# From Source
git clone https://github.com/Tecosys/nutaan-cli.git
cd nutaan-cli
pip install -e .
```

### Configuration
Create a `.env` file in your project root or home directory:

```env
# OpenAI (Default)
OPENAI_API_KEY=sk-...

# Anthropic (Optional)
ANTHROPIC_API_KEY=sk-ant-...

# Google (Optional)
GOOGLE_API_KEY=AIza...

# Brave Search (Required for web search)
BRAVE_SEARCH_API_KEY=...
```

## 4. Usage Guide

### Basic Commands
```bash
# Start interactive session
nutaan

# Single command
nutaan "Create a python script to calculate fibonacci"

# Think mode (for complex tasks)
nutaan --think "Analyze the security implications of this code"
```

### Plan Management
Nutaan includes a persistent plan manager.
```bash
# Create a plan
nutaan "Create a plan for 'Website Migration' with tasks: Backup DB, Copy files, Update DNS"

# View plans
nutaan "List my plans"

# Update progress
nutaan "Mark 'Backup DB' as complete"
```

### Available Tools
- **Think**: Log thoughts and reasoning steps.
- **Plan**: Manage project tasks.
- **Web Search**: Search the internet using Brave Search.
- **File Ops**: Read, write, and edit files safely.
- **Bash**: Execute shell commands.

## 5. Architecture

### Core Components

#### Agent Manager (`nutaan/core/agent_manager.py`)
- Orchestrates the creation of LangChain agents.
- Initializes tools and binds them to the agent.
- Manages session state and memory.

#### LLM Manager (`nutaan/core/llm_manager.py`)
- Handles initialization of different LLM providers.
- Implements fallback logic (e.g., if OpenAI fails, try Anthropic).
- Manages model configurations via environment variables.

#### Plan Tool (`nutaan/tools/plan_tool.py`)
- Implements a persistent todo list system.
- Stores data in `.nutaan_data/plans.json`.
- Supports hierarchical tasks and completion tracking.

### Data Flow
1. **User Input**: CLI receives command/prompt.
2. **Agent Creation**: `AgentManager` creates/retrieves an agent for the session.
3. **Reasoning**: Agent uses LLM to decide on actions (Think, Plan, Tool calls).
4. **Execution**: Tools execute actions (File I/O, Search, etc.).
5. **Response**: Agent formulates a final response.
6. **UI Display**: `UIManager` renders the response with Rich formatting.

## 6. Development

### Running Tests
```bash
python -m pytest
```

### Adding a New Tool
1. Create a new file in `nutaan/tools/`.
2. Inherit from `BaseTool`.
3. Implement `_run` method.
4. Register the tool in `nutaan/core/agent_manager.py`.

### Code Style
- Follow PEP 8.
- Use type hints.
- Add docstrings for classes and methods.

## 7. Configuration Reference

| Environment Variable | Description |
|----------------------|-------------|
| `OPENAI_API_KEY` | API key for OpenAI models |
| `ANTHROPIC_API_KEY` | API key for Claude models |
| `GOOGLE_API_KEY` | API key for Gemini models |
| `BRAVE_SEARCH_API_KEY` | API key for web search |
| `OPENAI_MODELS` | Comma-separated list of allowed OpenAI models |
| `ANTHROPIC_MODELS` | Comma-separated list of allowed Anthropic models |

## 8. Common Commands (Cheatsheet)

- `nutaan --help`: Show help message.
- `nutaan --version`: Show version.
- `nutaan --history`: View session history.
- `nutaan --stats`: View usage statistics.
- `nutaan --think`: Enable think mode.
