# MCP Terminal Server

> A comprehensive Model Context Protocol (MCP) server that provides Claude AI with secure access to your local terminal, file system, and system information through a rich set of structured tools.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.12.2+-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](#license)

## ✨ Features

### 🛡️ Terminal Operations
- **Secure Command Execution** - Run terminal commands with user-level permissions
- **Directory Management** - Navigate and manage working directory state
- **Cross-Platform Support** - Works seamlessly on Windows, macOS, and Linux
- **Smart Encoding** - Handles international characters with automatic encoding detection

### 📁 File System Operations
- **File Management** - Create, read, update, delete, copy, and move files
- **Directory Operations** - Create, list, copy, and delete directories
- **File Search** - Find files using glob patterns with recursive search
- **Content Search** - Search for text within files with pattern matching
- **File Information** - Get detailed metadata including permissions, dates, and sizes

### 🔍 System Information
- **System Details** - Platform, OS, hardware, and Python environment info
- **Environment Variables** - Read and set environment variables with filtering
- **Disk Usage** - Monitor disk space usage with human-readable formatting
- **Directory Listings** - Detailed directory contents with optional metadata

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** - [Download here](https://python.org/downloads/)
- **uv package manager** - [Install guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Claude Desktop** - [Download here](https://claude.ai/download)

### Installation Methods

#### Method 1: Using uvx (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mcp-terminal
   ```

2. **Configure Claude Desktop:**
   
   Edit your Claude Desktop config file:
   
   | Platform | Config Location |
   |----------|----------------|
   | Windows | `%APPDATA%\\Claude\\claude_desktop_config.json` |
   | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
   | Linux | `~/.config/Claude/claude_desktop_config.json` |

   Add this configuration (replace with your absolute path):
   ```json
   {
     "mcpServers": {
       "Terminal Server": {
         "command": "uvx",
         "args": [
           "--from",
           "C:\\dev\\mcp-terminal",
           "mcp-terminal"
         ]
       }
     }
   }
   ```

#### Method 2: Using uv run

Alternative configuration for running with uv directly:
```json
{
  "mcpServers": {
    "Terminal Server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\dev\\mcp-terminal\\src",
        "-m",
        "terminal"
      ]
    }
  }
}
```

3. **Start using with Claude:**
   - Restart Claude Desktop
   - Start a new conversation
   - Claude now has comprehensive terminal and file system access! 🎉

## 💡 Usage Examples

Once integrated, you can interact with your system through Claude naturally:

```
You: "What files are in my current directory?"
Claude: [Uses list_directory tool to show detailed directory contents]

You: "Create a Python script that prints 'Hello World' and run it"
Claude: [Uses create_file to create hello.py, then run_command to execute it]

You: "Find all Python files in this project"
Claude: [Uses find_files with "*.py" pattern to locate Python files]

You: "Search for the word 'FastMCP' in all files"
Claude: [Uses search_in_files to find text across the codebase]

You: "Show me system information and disk usage"
Claude: [Uses get_system_info and get_disk_usage to display system details]

You: "Copy my config file to a backup folder"
Claude: [Uses copy_file to create a backup copy]

You: "Set an environment variable for this session"
Claude: [Uses set_environment_variable to configure the environment]
```

## 🏗️ Project Structure

```
mcp-terminal/
├── 📄 README.md                        # This documentation
├── 📦 pyproject.toml                  # Project configuration and dependencies
├── 🔐 LICENSE                         # MIT License
├── 🔒 uv.lock                         # Dependency lock file
├── ⚙️ claude_desktop_config.json      # Example Claude Desktop configuration
└── 📁 src/terminal/                   # Source code directory
    ├── 📄 __init__.py                 # Package initialization
    ├── 🚀 __main__.py                 # Package entry point
    ├── 🖥️ server.py                   # FastMCP server with all tools
    └── 🔧 terminal.py                 # Command execution engine
```

## 🔌 Complete API Reference

### Terminal Operations

#### `run_command(command: str) -> command_result`
Executes terminal commands with full output capture. Automatically routes `cd` commands to directory management.

**Parameters:**
- `command`: Command string to execute

**Example:**
```python
run_command("ls -la")
run_command("git status") 
run_command("cd ../Documents")  # Automatically uses set_working_directory
```

#### `set_working_directory(path: str) -> command_result`
Changes the current working directory with persistent state management.

#### `get_working_directory() -> str`
Returns the current working directory path.

### File Operations

#### `create_file(file_path: str, content: str) -> command_result`
Creates a new file with specified content using UTF-8 encoding.

#### `read_file(file_path: str) -> command_result`
Reads and returns file content with UTF-8 encoding.

#### `append_to_file(file_path: str, content: str, add_newline: bool = True) -> command_result`
Appends content to an existing file, optionally adding a newline.

#### `delete_file(file_path: str) -> command_result`
Safely deletes a file with existence checking.

#### `copy_file(source_path: str, destination_path: str) -> command_result`
Copies a file from source to destination with directory creation.

#### `move_file_or_directory(source_path: str, destination_path: str) -> command_result`
Moves or renames files and directories.

### Directory Operations

#### `create_directory(directory_path: str) -> command_result`
Creates a directory with automatic parent directory creation.

#### `list_directory(path: str = ".", show_hidden: bool = False, show_details: bool = False) -> command_result`
Lists directory contents with optional detailed information.

#### `copy_directory(source_path: str, destination_path: str) -> command_result`
Recursively copies entire directories.

#### `delete_directory(directory_path: str, recursive: bool = False) -> command_result`
Deletes directories with optional recursive deletion.

### Search Operations

#### `find_files(pattern: str, search_path: str = ".", recursive: bool = True, case_sensitive: bool = True) -> command_result`
Searches for files using glob patterns with advanced options.

**Parameters:**
- `pattern`: Glob pattern (e.g., "*.py", "test_*.txt")
- `search_path`: Directory to search in
- `recursive`: Search subdirectories
- `case_sensitive`: Case-sensitive matching

#### `search_in_files(search_text: str, file_pattern: str = "*", search_path: str = ".", case_sensitive: bool = True, recursive: bool = True) -> command_result`
Searches for text within files matching a pattern.

### System Information

#### `get_file_info(file_path: str) -> command_result`
Gets comprehensive file/directory metadata including:
- Size, permissions, ownership
- Creation, modification, access times
- Type detection and symlink information

#### `get_system_info() -> command_result`
Returns detailed system information:
- Platform and OS details
- Python version and implementation
- User and environment information

#### `get_disk_usage(path: str = ".") -> command_result`
Provides disk usage statistics with human-readable formatting.

#### `get_environment_variables(filter_pattern: str = "") -> command_result`
Lists environment variables with optional filtering.

#### `set_environment_variable(name: str, value: str) -> command_result`
Sets environment variables for the current session.

### Response Format

All tools return a standardized `command_result` object:

```python
class command_result(BaseModel):
    success: bool = False              # Operation success status
    stdout: str = ""                   # Standard output or result content
    stderr: str = ""                   # Error output if any
    returncode: int = 1                # Exit code (0 = success)
    current_directory: str = os.getcwd()  # Current working directory
```

## 🔧 Development

### Testing the Server

Test the server directly:

```bash
# Using uvx
uvx --from C:\dev\mcp-terminal mcp-terminal

# Using uv run
uv run --directory C:\dev\mcp-terminal\src -m terminal

# Test with MCP inspector
npx @modelcontextprotocol/inspector uvx --from C:\dev\mcp-terminal mcp-terminal
```

### Adding Custom Tools

Extend functionality by adding tools to `src/terminal/server.py`:

```python
@mcp.tool()
def my_custom_tool(param: str) -> command_result:
    """
    Description of your custom tool.
    
    Args:
        param: Parameter description
        
    Returns:
        command_result: Result description
    """
    global current_directory
    try:
        # Your implementation here
        return command_result(
            success=True,
            stdout="Operation successful",
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
```

### Architecture Overview

- **Entry Point**: `src/terminal/__main__.py` - Package entry point that starts the server
- **Server Core**: `src/terminal/server.py` - FastMCP server with all tool implementations
- **Command Engine**: `src/terminal/terminal.py` - Low-level command execution with encoding handling
- **Package Configuration**: `pyproject.toml` - Defines `mcp-terminal = "terminal.__main__:main"`

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **Command not found errors** | Verify the command exists in your system PATH |
| **Permission denied** | Ensure proper file/directory permissions |
| **Encoding errors** | System uses automatic encoding detection - check locale settings |
| **Claude Desktop connection fails** | Verify absolute paths in config, restart Claude Desktop |
| **uvx/uv command not found** | Install uv package manager and ensure it's in PATH |
| **File operations fail** | Check file paths are correct and you have write permissions |

### Debug Commands

Test terminal functionality directly:
```bash
# Test command execution
python -c "
from src.terminal.terminal import terminal_run_command
result = terminal_run_command(['echo', 'Hello World'])
print(f'Success: {result.success}, Output: {result.stdout}')
"
```

### Configuration Validation

Verify your Claude Desktop configuration:
1. Use absolute paths (not relative)
2. Ensure proper JSON syntax
3. Restart Claude Desktop after changes
4. Check Claude Desktop logs for connection errors

## 🚀 Advanced Configuration

### Custom Environment Setup

```json
{
  "mcpServers": {
    "Terminal Server": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/to/mcp-terminal", "mcp-terminal"],
      "env": {
        "CUSTOM_VAR": "value",
        "PATH": "/custom/path:$PATH"
      }
    }
  }
}
```

### Security Considerations

- Commands execute with user-level permissions only
- No privilege escalation capabilities
- UTF-8 encoding enforced for file operations
- Path traversal protection via `os.path.join()` and `os.path.abspath()`
- Directory operations validate paths before execution

## 📝 Changelog

### v1.0.2 (Current)
- ✨ **Added comprehensive file operations**: create_file, read_file, append_to_file, delete_file, copy_file
- ✨ **Added advanced directory operations**: copy_directory, delete_directory, move_file_or_directory
- ✨ **Added powerful search capabilities**: find_files, search_in_files with pattern matching
- ✨ **Added detailed system information**: get_file_info, get_system_info, get_disk_usage
- ✨ **Added environment management**: get_environment_variables, set_environment_variable
- ✨ **Enhanced directory listings**: list_directory with optional details and hidden files
- 🔧 **Improved error handling** and path resolution across all operations
- 🔧 **Better encoding support** with UTF-8 enforcement for file operations

### v1.0.1
- ✨ Directory state management with persistent current_directory tracking
- ✨ Added change_working_directory and get_working_directory tools
- ✨ Automatic cd command routing to directory management
- 🔧 Enhanced command parsing with shlex.split()

### v1.0.0
- ✨ Initial release with FastMCP integration
- ✨ Cross-platform terminal command execution
- ✨ Multi-encoding detection for international character support
- ✨ Structured command results with Pydantic models

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow Python PEP 8 style guidelines
- Use comprehensive type hints and docstrings
- Handle errors gracefully with proper command_result responses  
- Maintain cross-platform compatibility
- Test thoroughly on different operating systems

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) for the specification
- [Anthropic](https://anthropic.com) for Claude and the MCP ecosystem
- [FastMCP](https://github.com/jlowin/fastmcp) for the server framework
- [uv](https://docs.astral.sh/uv/) for modern Python package management

---

**Made with ❤️ for the Claude community**

> Questions or suggestions? Open an issue or start a discussion!