from mcp.server.fastmcp import FastMCP
from terminal import run_command, command_result

mcp = FastMCP("Terminal MCP", "1.0.0")

@mcp.tool()
def run_command_tool(command: list[str] | str) -> command_result:
    """
    Runs a command in the terminal and returns the result.
    
    Args:
        command (list[str] | str): The command to run.
        
    Returns:
        command_result: The result of the command execution.
    """
    return run_command(command)
