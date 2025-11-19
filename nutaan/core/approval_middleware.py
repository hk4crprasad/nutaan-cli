"""
Approval Middleware - Human-in-the-loop tool approval using LangChain v1.0 middleware pattern
"""

from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from .tool_approval_manager import ToolApprovalManager, NotApproved


def create_approval_middleware(approval_manager: ToolApprovalManager):
    """
    Create middleware that requires human approval for dangerous tool calls.
    
    Uses the @wrap_tool_call decorator pattern from LangChain v1.0 to intercept
    tool executions and check for approval before proceeding.
    
    Args:
        approval_manager: ToolApprovalManager instance to handle approval logic
        
    Returns:
        Middleware function that wraps tool calls with approval checking
    """
    
    @wrap_tool_call
    def approval_middleware(request, handler):
        """
        Intercept tool calls and check for approval before execution.
        
        Args:
            request: ToolRequest containing tool call information
            handler: Next handler in the middleware chain (actual tool execution)
            
        Returns:
            ToolMessage with the tool result, or error if not approved
        """
        tool_name = request.tool_call.get("name", "unknown")
        tool_args = request.tool_call.get("args", {})
        
        # Check if this tool requires approval
        if tool_name in approval_manager.dangerous_tools:
            # Create a simple tool call dict for approval display
            tool_call_info = {
                "name": tool_name,
                "args": tool_args,
                "id": request.tool_call.get("id", "")
            }
            
            # Check approval
            approval_key = approval_manager._create_approval_key(tool_name, tool_args)
            
            # If not in cache, ask for approval
            if approval_key not in approval_manager.approvals:
                # Display approval request
                try:
                    approval_manager._display_approval_request([tool_call_info])
                except NotApproved as e:
                    # User denied the tool call
                    return ToolMessage(
                        content=f"❌ Tool execution denied: {str(e)}",
                        tool_call_id=request.tool_call.get("id", "")
                    )
            elif not approval_manager.approvals[approval_key]:
                # Previously denied
                return ToolMessage(
                    content=f"❌ Tool '{tool_name}' was previously denied",
                    tool_call_id=request.tool_call.get("id", "")
                )
        
        # Tool is safe or approved - execute it
        try:
            return handler(request)
        except Exception as e:
            # Handle tool execution errors
            return ToolMessage(
                content=f"❌ Tool execution error: {str(e)}",
                tool_call_id=request.tool_call.get("id", "")
            )
    
    return approval_middleware
