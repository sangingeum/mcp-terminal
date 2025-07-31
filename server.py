import os
import shlex
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
    command = command if isinstance(command, list) else shlex.split(command) # Ensure command is a list
    if command[0] == "cd":
        path = command[1] if len(command) > 1 else ""
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


@mcp.tool()
def create_file(file_path: str, content: str) -> command_result:
    """
    Creates a file with the specified content.
    
    Args:
        file_path (str): The path to the file to create.
        content (str): The content to write to the file.
        
    Returns:
        command_result: The result of the file creation command.
    """
    try:
        global current_directory
        file_path = os.path.join(current_directory, file_path)
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Write the content to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return command_result(
            success=True,
            stdout=f"File '{file_path}' created successfully.",
            stderr="",
            returncode=0,
            current_directory=current_directory
        )
    except Exception as e:
        return command_result(
            success=False,
            stdout="",
            stderr=str(e),
            returncode=1,
            current_directory=current_directory
        )

@mcp.tool()
def read_file(file_path: str) -> command_result:
    """
    Reads the content of a file.
    
    Args:
        file_path (str): The path to the file to read.
        
    Returns:
        command_result: The result of the file read command.
    """
    try:
        global current_directory
        file_path = os.path.join(current_directory, file_path)
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return command_result(
            success=True,
            stdout=content,
            stderr="",
            returncode=0,
            current_directory=current_directory
        )
    except Exception as e:
        return command_result(
            success=False,
            stdout="",
            stderr=str(e),
            returncode=1,
            current_directory=current_directory
        )
        
@mcp.tool()
def delete_file(file_path: str) -> command_result:
    """
    Deletes a file.
    
    Args:
        file_path (str): The path to the file to delete.
        
    Returns:
        command_result: The result of the file deletion command.
    """
    try:
        global current_directory
        file_path = os.path.join(current_directory, file_path)
        # Delete the file
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        os.remove(file_path)
        return command_result(
            success=True,
            stdout=f"File '{file_path}' deleted successfully.",
            stderr="",
            returncode=0,
            current_directory=current_directory
        )
    except Exception as e:
        return command_result(
            success=False,
            stdout="",
            stderr=str(e),
            returncode=1,
            current_directory=current_directory
        )
    