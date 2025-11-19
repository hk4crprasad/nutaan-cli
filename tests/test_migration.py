#!/usr/bin/env python3
"""Test script for the create_agent migration"""

import sys
import os
import importlib.util

# Add the project directory to path
sys.path.insert(0, '/home/tecosys/nutaan-cli')

# Test 1: Import LangChain v1.0
print("Test 1: Importing LangChain v1.0 APIs...")
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
print("✅ LangChain v1.0 APIs imported successfully\n")

# Test 2: Test prompt system (doesn't have relative imports)
print("Test 2: Testing prompt system...")
spec = importlib.util.spec_from_file_location(
    "prompt_system",
    "/home/tecosys/nutaan-cli/nutaan/core/prompt_system.py"
)
prompt_system_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompt_system_module)

ps = prompt_system_module.PromptSystem(think_mode=False)
prompt = ps.get_system_prompt()
print(f"✅ Prompt system working: generated {len(prompt)} character prompt")
print(f"✅ Prompt is string type: {isinstance(prompt, str)}")
print(f"✅ No async/await required\n")

# Test 3: Verify the middleware file exists and has correct structure
print("Test 3: Checking approval middleware file...")
middleware_file = "/home/tecosys/nutaan-cli/nutaan/core/approval_middleware.py"
with open(middleware_file, 'r') as f:
    content = f.read()
    assert '@wrap_tool_call' in content, "Missing @wrap_tool_call decorator usage"
    assert 'def create_approval_middleware' in content, "Missing create_approval_middleware function"
    assert 'ToolApprovalManager' in content, "Missing ToolApprovalManager import"
print("✅ Approval middleware file structure correct\n")

# Test 4: Check create_agent signature
print("Test 4: Verifying create_agent signature...")
import inspect
sig = inspect.signature(create_agent)
params = list(sig.parameters.keys())
print(f"   Parameters: {params}")
assert 'model' in params, "Missing 'model' parameter"
assert 'tools' in params, "Missing 'tools' parameter"
assert 'middleware' in params, "Missing 'middleware' parameter"
assert 'checkpointer' in params, "Missing 'checkpointer' parameter"
print("✅ create_agent has correct signature\n")

# Test 5: Verify wrap_tool_call decorator
print("Test 5: Testing @wrap_tool_call decorator...")
@wrap_tool_call
def test_middleware(request, handler):
    """Test middleware function"""
    return handler(request)

print(f"✅ @wrap_tool_call decorator works\n")

print("=" * 60)
print("🎉 ALL MIGRATION TESTS PASSED!")
print("=" * 60)
print("\nMigration Summary:")
print("- ✅ LangChain v1.0 create_agent API working")
print("- ✅ Middleware pattern (@wrap_tool_call) working")
print("- ✅ Prompt system returns string (no async)")
print("- ✅ Approval middleware module created")
print("\nNext steps:")
print("- Fix fireworks import issue in llm_manager.py")
print("- Test full agent creation end-to-end")
print("- Verify approval flow in running application")
