# Nutaan CLI - AI Agent Instructions

## Project Overview
Nutaan-CLI is a ReAct (Reasoning and Acting) Python assistant powered by LangChain v1.0+ and LangGraph. It features a human-in-the-loop approval system via middleware, persistent task management, and a rich terminal UI.

**Key Architecture**: CLI → Agent Manager → LangChain Agent (create_agent) → Middleware → Tools

## Critical Architecture Patterns

### 1. Human-in-the-Loop Approval System (Middleware Pattern)
All dangerous tools (`bash_run`, `file_write`, `file_edit`) require user approval before execution using the **middleware pattern**.

**Flow**: Tool call → Approval Middleware (@wrap_tool_call) → ToolApprovalManager → User prompt → Tool execution
- Uses `@wrap_tool_call` decorator from `langchain.agents.middleware`
- Approvals persist in `tool_approvals.json`
- Safe tools (`file_read`, `brave_web_search`, `think`, `plan`) bypass approval
- See `nutaan/core/approval_middleware.py` for middleware implementation
- See `nutaan/core/tool_approval_manager.py` for approval logic

**When modifying tools**: Update `dangerous_tools` or `safe_tools` sets in `ToolApprovalManager.__init__`

**Key difference from old approach**: No wrapper class - middleware intercepts at tool execution level

### 2. Multi-Model LLM System
`nutaan/core/llm_manager.py` provides automatic fallback across 10+ LLM providers (OpenAI, Anthropic, Google, Groq, Ollama, etc.).

**Model selection priority**:
1. User-specified via `--set-model` (stored in config)
2. First available from environment variables
3. Automatic fallback to next available

**Key files**:
- Environment setup: `ENVIRONMENT.md`, `.env.example`
- Configuration: `nutaan/core/config_manager.py`
- Commands: `--list-models`, `--current-model`, `--set-model`

### 3. File Edit Safety Protocol
Files MUST be read before editing - enforced by `FileTimestampManager` (singleton).

**Workflow**:
1. `file_read` → Updates timestamp in manager
2. `file_edit` → Checks timestamp before allowing edits
3. Shows rich diff preview before applying changes

**Implementation**: `nutaan/tools/file_timestamp_manager.py` tracks read timestamps globally

### 4. Plan Tool Architecture
Plans are persistent todo lists stored in `.nutaan_data/plans.json` with strikethrough formatting for completed items.

**Key pattern**: Plan operations return formatted Unicode art with checkboxes:
- `☐` Incomplete items
- `☑` Completed items (with strikethrough text in terminal)
- Progress bars show completion percentage

**Tool commands**: `create plan`, `complete item`, `add item`, `list plans`, `show plan`

## Development Workflows

### Running the Application
```bash
# Interactive mode
nutaan

# With custom environment
nutaan -e .env.production

# Direct prompt execution
nutaan "your prompt here"

# Think mode (enhanced reasoning)
nutaan --think "complex problem"
```

### Testing & Development
```bash
# Install in editable mode
pip install -e .

# Test with different models
nutaan -e .env.development --list-models
nutaan --set-model groq llama-3.3-70b-versatile

# Reset approvals during testing
nutaan --reset-approvals
```

### Package Distribution
```bash
# Build package
python -m build

# Install from PyPI
pip install nutaan-cli
```

## Project-Specific Conventions

### Tool Implementation Pattern
All tools inherit from `langchain_core.tools.BaseTool`:

```python
class MyTool(BaseTool):
    name: str = "tool_name"  # Snake_case
    description: str = "..."  # Must describe input format clearly
    
    def _run(self, param: str) -> str:
        # Implementation
        return "result"
```

**Important**: Tool descriptions must specify exact input format (see `file_edit`: `'filepath|old_text|new_text'`)

### Prompt System Philosophy
`nutaan/core/prompt_system.py` enforces:
- **Defensive security only**: Refuse malicious code generation
- **Concise responses**: <4 lines unless detail requested
- **No comments**: Code should be self-documenting (unless asked)
- **Plan-first approach**: Use plan tool before multi-step tasks
- **Think-first pattern**: Use think tool for complex reasoning

### Rich UI Standards
All user-facing output uses Rich library for formatting:
- Panels for sections (`Panel.fit()`)
- Syntax highlighting for code (`Syntax()`)
- Markdown rendering for diffs
- Progress indicators for plans

**Fallback**: All Rich formatting degrades gracefully when library unavailable

## Key Integration Points

### Agent Creation Flow (LangChain v1.0)
```
cli.py:main() 
  → agent_manager.create_agent(think_mode, session_id)
    → LLM from llm_manager.get_best_available_llm()
    → Tools initialized (7 core tools)
    → System prompt from PromptSystem.get_system_prompt()
    → Approval middleware from create_approval_middleware()
    → create_agent(model, tools, system_prompt, middleware, checkpointer)
    → Returns LangGraph-based agent with middleware
```

**Key components**:
- `create_agent()` from `langchain.agents` (not `langgraph.prebuilt.create_react_agent`)
- Middleware list includes approval middleware
- MemorySaver checkpointer for conversation history
- System prompt passed directly as string parameter

### Session Management
- History: In-memory during runtime (via `MemorySaver`)
- Plans: Persistent in `.nutaan_data/plans.json`
- Approvals: Persistent in `tool_approvals.json`
- Config: `~/.nutaan_config.json` for model preferences

### Environment Variable Pattern
Use `python-dotenv` for configuration:
- Default: `.env` in current directory
- Custom: `--env path/to/.env`
- Provider-specific: `{PROVIDER}_API_KEY` naming convention

## Common Tasks

### Adding a New Tool
1. Create tool file in `nutaan/tools/` extending `BaseTool`
2. Add to `agent_manager._initialize_tools()` list
3. Classify in `ToolApprovalManager` (safe vs dangerous)
4. Update README tool list

### Adding a New LLM Provider
1. Add import in `nutaan/core/llm_manager.py` with try/except
2. Create `ModelConfig` in `_get_all_model_configs()`
3. Add initialization logic in `_initialize_provider()`
4. Update `ENVIRONMENT.md` with new variables

### Modifying Approval Behavior
Edit `ToolApprovalManager._display_tool_call()` for tool-specific formatting
Add entries to `dangerous_tools` or `safe_tools` sets in `__init__`

## Critical Files Reference
- **Entry point**: `nutaan/cli.py:main()` - Argument parsing and command routing
- **Agent orchestration**: `nutaan/core/agent_manager.py` - Agent lifecycle using create_agent
- **LLM abstraction**: `nutaan/core/llm_manager.py` - Multi-provider support  
- **Approval middleware**: `nutaan/core/approval_middleware.py` - @wrap_tool_call decorator
- **Approval manager**: `nutaan/core/tool_approval_manager.py` - Human-in-the-loop logic
- **System prompts**: `nutaan/core/prompt_system.py` - Behavior guidelines
- **Plan persistence**: `nutaan/tools/plan_tool.py` - Task management logic

## Dependencies & Compatibility
- **Python**: >=3.8
- **Core**: LangChain 1.0+, LangGraph 0.5+, Rich 13+
- **Optional**: All LLM provider libraries (graceful fallback)
- **Installation**: PyPI (`nutaan-cli`) or source (`pip install -e .`)
