import os
import shlex
import shutil
import stat
import sys
import platform
import glob
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from .terminal import terminal_run_command, command_result

mcp = FastMCP("Terminal MCP", "1.0.2")
current_directory = os.getcwd() # Initialize with the current working directory

@mcp.tool()
def run_command(command: str) -> command_result:
    """
    Runs a command in the terminal and returns the result.
    
    Args:
        command (str): The command to run.
        
    Returns:
        command_result: The result of the command execution.
    """
    # If the command is a change directory command,
    global current_directory
    command = shlex.split(command) # Ensure command is a list
    if command[0] == "cd":
        path = command[1] if len(command) > 1 else ""
        return set_working_directory(path)
    else:
        return terminal_run_command(command, current_directory, change_directory=False)

@mcp.tool()
def set_working_directory(path: str) -> command_result:
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
def get_working_directory() -> str:
    """
    Returns the current working directory.
    
    Returns:
        str: The current working directory.
    """
    global current_directory 
    return current_directory

@mcp.tool()
def create_directory(directory_path: str) -> command_result:
    """
    Creates a directory at the specified path.
    
    Args:
        directory_path (str): The path to the directory to create.
        
    Returns:
        command_result: The result of the directory creation command.
    """
    try:
        global current_directory
        directory_path = os.path.join(current_directory, directory_path)
        os.makedirs(directory_path, exist_ok=True)
        return command_result(
            success=True,
            stdout=f"Directory '{directory_path}' created successfully.",
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
def append_to_file(file_path: str, content: str, add_newline: bool = True) -> command_result:
    """
    Appends content to a file, optionally adding a newline.
    
    Args:
        file_path (str): The path to the file to append to.
        content (str): The content to append.
        add_newline (bool): Whether to add a newline before appending (default: True).
        
    Returns:
        command_result: The result of the append operation.
    """
    try:
        global current_directory
        file_path = os.path.join(current_directory, file_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'a', encoding='utf-8') as f:
            if add_newline:
                f.write("\n")
            f.write(content)
        
        return command_result(
            success=True,
            stdout=f"Content appended to '{file_path}' successfully.",
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

@mcp.tool()
def copy_file(source_path: str, destination_path: str) -> command_result:
    """
    Copies a file from source to destination.
    
    Args:
        source_path (str): The path of the source file.
        destination_path (str): The path of the destination file.
        
    Returns:
        command_result: The result of the file copy operation.
    """
    try:
        global current_directory
        source_path = os.path.join(current_directory, source_path)
        destination_path = os.path.join(current_directory, destination_path)
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file '{source_path}' does not exist.")
        
        if os.path.isdir(source_path):
            raise IsADirectoryError(f"'{source_path}' is a directory. Use copy_directory for directories.")
        
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        shutil.copy2(source_path, destination_path)
        
        return command_result(
            success=True,
            stdout=f"File copied from '{source_path}' to '{destination_path}' successfully.",
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
def find_files(pattern: str, search_path: str = ".", recursive: bool = True, case_sensitive: bool = True) -> command_result:
    """
    Searches for files matching a pattern using glob syntax.
    
    Args:
        pattern (str): The glob pattern to search for (e.g., "*.py", "test_*.txt").
        search_path (str): The directory to search in (default: current directory).
        recursive (bool): Whether to search recursively in subdirectories.
        case_sensitive (bool): Whether the search should be case sensitive.
        
    Returns:
        command_result: The result containing matching file paths.
    """
    try:
        global current_directory
        search_path = os.path.join(current_directory, search_path)
        search_path = os.path.abspath(search_path)
        
        if not os.path.exists(search_path):
            raise FileNotFoundError(f"Search path '{search_path}' does not exist.")
        
        if recursive:
            search_pattern = os.path.join(search_path, "**", pattern)
            matches = glob.glob(search_pattern, recursive=True)
        else:
            search_pattern = os.path.join(search_path, pattern)
            matches = glob.glob(search_pattern)
        
        if not case_sensitive and sys.platform != "win32":
            # For case-insensitive search on non-Windows systems
            import fnmatch
            all_files = []
            if recursive:
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        all_files.append(os.path.join(root, file))
            else:
                all_files = [os.path.join(search_path, f) for f in os.listdir(search_path) 
                           if os.path.isfile(os.path.join(search_path, f))]
            
            matches = [f for f in all_files if fnmatch.fnmatch(os.path.basename(f).lower(), pattern.lower())]
        
        # Convert to relative paths for cleaner output
        relative_matches = []
        for match in matches:
            try:
                rel_path = os.path.relpath(match, current_directory)
                relative_matches.append(rel_path)
            except ValueError:
                # If relative path can't be computed, use absolute path
                relative_matches.append(match)
        
        output = "\
".join(sorted(relative_matches)) if relative_matches else "No files found matching the pattern."
        
        return command_result(
            success=True,
            stdout=output,
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
def search_in_files(search_text: str, file_pattern: str = "*", search_path: str = ".", case_sensitive: bool = True, recursive: bool = True) -> command_result:
    """
    Searches for text within files matching a pattern.
    
    Args:
        search_text (str): The text to search for.
        file_pattern (str): The file pattern to search in (default: "*" for all files).
        search_path (str): The directory to search in (default: current directory).
        case_sensitive (bool): Whether the search should be case sensitive.
        recursive (bool): Whether to search recursively in subdirectories.
        
    Returns:
        command_result: The result containing search results with file paths and line numbers.
    """
    try:
        global current_directory
        search_path = os.path.join(current_directory, search_path)
        search_path = os.path.abspath(search_path)
        
        if not os.path.exists(search_path):
            raise FileNotFoundError(f"Search path '{search_path}' does not exist.")
        
        # Get matching files
        if recursive:
            pattern_path = os.path.join(search_path, "**", file_pattern)
            files = glob.glob(pattern_path, recursive=True)
        else:
            pattern_path = os.path.join(search_path, file_pattern)
            files = glob.glob(pattern_path)
        
        # Filter to only include actual files
        files = [f for f in files if os.path.isfile(f)]
        
        results = []
        search_term = search_text if case_sensitive else search_text.lower()
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        line_to_check = line if case_sensitive else line.lower()
                        if search_term in line_to_check:
                            rel_path = os.path.relpath(file_path, current_directory)
                            results.append(f"{rel_path}:{line_num}: {line.rstrip()}")
            except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                # Skip files that can't be read
                continue
        
        if results:
            output = f"Found {len(results)} matches:\
" + "\
".join(results)
        else:
            output = f"No matches found for '{search_text}' in files matching '{file_pattern}'"
        
        return command_result(
            success=True,
            stdout=output,
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
def get_file_info(file_path: str) -> command_result:
    """
    Gets detailed information about a file or directory.
    
    Args:
        file_path (str): The path of the file or directory to inspect.
        
    Returns:
        command_result: The result containing file information.
    """
    try:
        global current_directory
        file_path = os.path.join(current_directory, file_path)
        file_path = os.path.abspath(file_path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Path '{file_path}' does not exist.")
        
        stat_info = os.stat(file_path)
        is_dir = os.path.isdir(file_path)
        is_file = os.path.isfile(file_path)
        is_link = os.path.islink(file_path)
        
        info = {
            "path": file_path,
            "type": "directory" if is_dir else "file" if is_file else "other",
            "size": stat_info.st_size,
            "permissions": stat.filemode(stat_info.st_mode),
            "owner_uid": stat_info.st_uid,
            "group_gid": stat_info.st_gid,
            "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
            "is_symlink": is_link
        }
        
        if is_link:
            info["link_target"] = os.readlink(file_path)
        
        if is_dir:
            try:
                contents = os.listdir(file_path)
                info["item_count"] = len(contents)
            except PermissionError:
                info["item_count"] = "Permission denied"
        
        # Format output as readable text
        output_lines = [
            f"Path: {info['path']}",
            f"Type: {info['type']}",
            f"Size: {info['size']} bytes",
            f"Permissions: {info['permissions']}",
            f"Owner UID: {info['owner_uid']}",
            f"Group GID: {info['group_gid']}",
            f"Created: {info['created']}",
            f"Modified: {info['modified']}",
            f"Accessed: {info['accessed']}",
            f"Is Symlink: {info['is_symlink']}"
        ]
        
        if info['is_symlink']:
            output_lines.append(f"Link Target: {info['link_target']}")
        
        if 'item_count' in info:
            output_lines.append(f"Items in Directory: {info['item_count']}")
        
        return command_result(
            success=True,
            stdout="\
".join(output_lines),
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
def list_directory(path: str = ".", show_hidden: bool = False, show_details: bool = False) -> command_result:
    """
    Lists the contents of a directory with optional detailed information.
    
    Args:
        path (str): The directory path to list (default: current directory).
        show_hidden (bool): Whether to show hidden files and directories.
        show_details (bool): Whether to show detailed file information (size, permissions, dates).
        
    Returns:
        command_result: The result containing directory listing.
    """
    try:
        global current_directory
        target_path = os.path.join(current_directory, path) if path != "." else current_directory
        target_path = os.path.abspath(target_path)
        
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Directory '{target_path}' does not exist.")
        
        if not os.path.isdir(target_path):
            raise NotADirectoryError(f"'{target_path}' is not a directory.")
        
        items = []
        for item in os.listdir(target_path):
            if not show_hidden and item.startswith('.'):
                continue
            
            item_path = os.path.join(target_path, item)
            
            if show_details:
                stat_info = os.stat(item_path)
                is_dir = os.path.isdir(item_path)
                size = stat_info.st_size if not is_dir else 0
                modified = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                # Get permissions in readable format
                mode = stat.filemode(stat_info.st_mode)
                
                item_info = f"{mode} {size:>10} {modified} {item}{'/' if is_dir else ''}"
            else:
                item_info = f"{item}{'/' if os.path.isdir(item_path) else ''}"
            
            items.append(item_info)
        
        output = "\
".join(sorted(items)) if items else "Directory is empty"
        
        return command_result(
            success=True,
            stdout=output,
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
def copy_directory(source_path: str, destination_path: str) -> command_result:
    """
    Copies a directory recursively from source to destination.
    
    Args:
        source_path (str): The path of the source directory.
        destination_path (str): The path of the destination directory.
        
    Returns:
        command_result: The result of the directory copy operation.
    """
    try:
        global current_directory
        source_path = os.path.join(current_directory, source_path)
        destination_path = os.path.join(current_directory, destination_path)
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source directory '{source_path}' does not exist.")
        
        if not os.path.isdir(source_path):
            raise NotADirectoryError(f"'{source_path}' is not a directory.")
        
        if os.path.exists(destination_path):
            raise FileExistsError(f"Destination '{destination_path}' already exists.")
        
        shutil.copytree(source_path, destination_path)
        
        return command_result(
            success=True,
            stdout=f"Directory copied from '{source_path}' to '{destination_path}' successfully.",
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
def delete_directory(directory_path: str, recursive: bool = False) -> command_result:
    """
    Deletes a directory.
    
    Args:
        directory_path (str): The path of the directory to delete.
        recursive (bool): Whether to delete the directory recursively (with all contents).
        
    Returns:
        command_result: The result of the directory deletion operation.
    """
    try:
        global current_directory
        directory_path = os.path.join(current_directory, directory_path)
        
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory '{directory_path}' does not exist.")
        
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"'{directory_path}' is not a directory.")
        
        if recursive:
            shutil.rmtree(directory_path)
            message = f"Directory '{directory_path}' and all its contents deleted successfully."
        else:
            os.rmdir(directory_path)
            message = f"Directory '{directory_path}' deleted successfully."
        
        return command_result(
            success=True,
            stdout=message,
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
def move_file_or_directory(source_path: str, destination_path: str) -> command_result:
    """
    Moves (renames) a file or directory from source to destination.
    
    Args:
        source_path (str): The path of the source file or directory.
        destination_path (str): The path of the destination file or directory.
        
    Returns:
        command_result: The result of the move operation.
    """
    try:
        global current_directory
        source_path = os.path.join(current_directory, source_path)
        destination_path = os.path.join(current_directory, destination_path)
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source '{source_path}' does not exist.")
        
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        shutil.move(source_path, destination_path)
        
        return command_result(
            success=True,
            stdout=f"'{source_path}' moved to '{destination_path}' successfully.",
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
def get_disk_usage(path: str = ".") -> command_result:
    """
    Gets disk usage information for a path.
    
    Args:
        path (str): The path to check disk usage for (default: current directory).
        
    Returns:
        command_result: The result containing disk usage information.
    """
    try:
        global current_directory
        path = os.path.join(current_directory, path)
        path = os.path.abspath(path)
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path '{path}' does not exist.")
        
        usage = shutil.disk_usage(path)
        
        def format_bytes(bytes_val):
            """Convert bytes to human readable format"""
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes_val < 1024.0:
                    return f"{bytes_val:.1f} {unit}"
                bytes_val /= 1024.0
            return f"{bytes_val:.1f} PB"
        
        total = usage.total
        used = usage.used
        free = usage.free
        percent_used = (used / total) * 100 if total > 0 else 0
        
        output_lines = [
            f"Disk Usage for: {path}",
            f"Total: {format_bytes(total)} ({total:,} bytes)",
            f"Used: {format_bytes(used)} ({used:,} bytes)",
            f"Free: {format_bytes(free)} ({free:,} bytes)",
            f"Usage: {percent_used:.1f}%"
        ]
        
        return command_result(
            success=True,
            stdout="\
".join(output_lines),
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
def get_system_info() -> command_result:
    """
    Gets system information including OS, Python version, and environment details.
    
    Returns:
        command_result: The result containing system information.
    """
    try:
        global current_directory
        
        info = {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "current_directory": current_directory,
            "user": os.environ.get("USER") or os.environ.get("USERNAME", "Unknown"),
            "home_directory": os.path.expanduser("~"),
            "path_separator": os.sep,
            "environment_variables_count": len(os.environ)
        }
        
        output_lines = [
            f"Platform: {info['platform']}",
            f"System: {info['system']}",
            f"Release: {info['release']}",
            f"Version: {info['version']}",
            f"Machine: {info['machine']}",
            f"Processor: {info['processor']}",
            f"Python Version: {info['python_version']}",
            f"Python Implementation: {info['python_implementation']}",
            f"Current Directory: {info['current_directory']}",
            f"User: {info['user']}",
            f"Home Directory: {info['home_directory']}",
            f"Path Separator: {info['path_separator']}",
            f"Environment Variables: {info['environment_variables_count']}"
        ]
        
        return command_result(
            success=True,
            stdout="\
".join(output_lines),
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
def get_environment_variables(filter_pattern: str = "") -> command_result:
    """
    Gets environment variables, optionally filtered by a pattern.
    
    Args:
        filter_pattern (str): Optional pattern to filter environment variable names (case-insensitive).
        
    Returns:
        command_result: The result containing environment variables.
    """
    try:
        global current_directory
        
        env_vars = dict(os.environ)
        
        if filter_pattern:
            filtered_vars = {
                key: value for key, value in env_vars.items()
                if filter_pattern.lower() in key.lower()
            }
        else:
            filtered_vars = env_vars
        
        if not filtered_vars:
            output = f"No environment variables found" + (f" matching '{filter_pattern}'" if filter_pattern else "")
        else:
            output_lines = [f"{key}={value}" for key, value in sorted(filtered_vars.items())]
            count = len(filtered_vars)
            header = f"Found {count} environment variable{'s' if count != 1 else ''}" + (f" matching '{filter_pattern}'" if filter_pattern else "") + ":\
"
            output = header + "\
".join(output_lines)
        
        return command_result(
            success=True,
            stdout=output,
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
def set_environment_variable(name: str, value: str) -> command_result:
    """
    Sets an environment variable for the current session.
    
    Args:
        name (str): The name of the environment variable.
        value (str): The value to set.
        
    Returns:
        command_result: The result of setting the environment variable.
    """
    try:
        global current_directory
        
        os.environ[name] = value
        
        return command_result(
            success=True,
            stdout=f"Environment variable '{name}' set to '{value}'",
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

