import os
from mcp.server.fastmcp import FastMCP
from terminal import terminal_run_command, command_result

mcp = FastMCP("Terminal MCP", "1.0.2")
current_directory = os.getcwd() # Initialize with the current working directory

@mcp.tool()
def change_directory(path: str) -> command_result:
    """
    Changes the current working directory.
    
    Args:
        path (str): The path to change to.
        
    Returns:
        command_result: The result of the change directory command.
    """
    global current_directory 
    result = terminal_run_command(["cd", path], cwd=current_directory, change_directory=True)
    current_directory = result.current_directory  # Update the global current directory
    return result

@mcp.tool()
def run_command(command: list[str] | str) -> command_result:
    """
    Runs a command in the terminal and returns the result.
    
    Args:
        command (list[str] | str): The command to run.
        
    Returns:
        command_result: The result of the command execution.
    """
    # If the command is a change directory command,
    global current_directory
    if (isinstance(command, list) and command[0] == "cd"):
        path = command[1] if len(command) > 1 else ""
        return change_directory(path)
    if (isinstance(command, str) and command.startswith("cd ")):
        path = command[3:]
        return change_directory(path)
    else:
        return terminal_run_command(command, current_directory, change_directory=False)

@mcp.tool()
def get_current_directory() -> str:
    """
    Returns the current working directory.
    
    Returns:
        str: The current working directory.
    """
    global current_directory 
    return current_directory
