# MCP Terminal Server

> A secure Model Context Protocol (MCP) server that bridges Claude AI with your local terminal and file system, enabling safe command execution and file operations through a structured interface.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.12.2+-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](#license)

## ✨ Features

- 🛡️ **Secure Execution** - Commands run with user-level permissions only
- 🌍 **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux
- 🔤 **Smart Encoding** - Handles international characters with multiple encoding detection
- 📊 **Structured Results** - Returns detailed command output with status codes
- 🎯 **Directory Tracking** - Maintains current working directory state across operations
- 📁 **File Operations** - Create, read, and delete files with UTF-8 encoding
- 📂 **Directory Management** - Create directories and navigate file system
- ⚡ **Fast Integration** - Quick setup with Claude Desktop using uvx

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** - [Download here](https://python.org/downloads/)
- **uv package manager** - [Install guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Claude Desktop** - [Download here](https://claude.ai/download)

### Installation

The project uses modern Python packaging with uvx, so no manual installation is required:

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
           "/absolute/path/to/mcp-terminal",
           "mcp-terminal"
         ]
       }
     }
   }
   ```

3. **Start using with Claude:**
   - Restart Claude Desktop
   - Start a new conversation
   - Claude now has terminal and file system access! 🎉

## 💡 Usage Examples

Once integrated, you can interact with your terminal and file system through Claude naturally:

```
You: "What files are in my current directory?"
Claude: [Executes directory listing command and shows results]

You: "Create a Python file called hello.py that prints 'Hello World'"
Claude: [Creates the file with the specified content]

You: "Show me the git status of this repository"
Claude: [Runs `git status` and explains the output]

You: "Navigate to my Documents folder and list the contents"
Claude: [Changes directory and lists files]

You: "Read the contents of config.json"
Claude: [Uses read_file tool to show file contents]

You: "Create a new directory called 'projects'"
Claude: [Creates the directory using create_directory tool]
```

## 🏗️ Project Structure

```
mcp-terminal/
├── 📄 README.md                        # This documentation
├── 📦 pyproject.toml                  # Project configuration and dependencies
├── 🔐 LICENSE                         # MIT License
├── 🐍 .python-version                 # Python version requirement (3.13)
├── 🔒 uv.lock                         # Dependency lock file
├── ⚙️ claude_desktop_config.json      # Example Claude Desktop configuration
├── 🙈 .gitignore                      # Git ignore rules
└── 📁 src/terminal/                   # Source code directory
    ├── 📄 __init__.py                 # Package initialization
    ├── 🚀 main.py                     # MCP server entry point
    ├── 🖥️ server.py                   # FastMCP server with tools
    └── 🔧 terminal.py                 # Command execution engine
```

## 🔌 API Reference

### Core Tools

#### `run_command(command: str | list[str]) -> command_result`
Executes terminal commands with full output capture. Automatically handles `cd` commands by routing them to `change_working_directory`.

**Parameters:**
- `command`: Command string or list of command parts

**Returns:**
- `command_result` object with execution details

**Example:**
```python
# As string
run_command("ls -la")

# As list
run_command(["git", "status"])

# Directory changes are handled automatically
run_command("cd ../Documents")
```

#### `change_working_directory(path: str) -> command_result`
Changes the current working directory with state persistence across tool calls.

**Parameters:**
- `path`: Target directory path (relative or absolute)

**Returns:**
- `command_result` object with updated directory state

#### `get_current_directory() -> str`
Returns the current working directory path.

**Returns:**
- `str`: Current directory path

### File Operations

#### `create_file(file_path: str, content: str) -> command_result`
Creates a new file with specified content using UTF-8 encoding. Automatically creates parent directories if needed.

**Parameters:**
- `file_path`: Path to the file to create (relative to current directory)
- `content`: Content to write to the file

**Returns:**
- `command_result` object with creation status

#### `read_file(file_path: str) -> command_result`
Reads and returns the content of a file using UTF-8 encoding.

**Parameters:**
- `file_path`: Path to the file to read (relative to current directory)

**Returns:**
- `command_result` object with file content in stdout

#### `delete_file(file_path: str) -> command_result`
Deletes a specified file with existence checking.

**Parameters:**
- `file_path`: Path to the file to delete (relative to current directory)

**Returns:**
- `command_result` object with deletion status

### Directory Operations

#### `create_directory(directory_path: str) -> command_result`
Creates a new directory at the specified path with `exist_ok=True`.

**Parameters:**
- `directory_path`: Path to the directory to create (relative to current directory)

**Returns:**
- `command_result` object with creation status

### Response Format

All tools return a `command_result` Pydantic model with the following structure:

```python
class command_result(BaseModel):
    success: bool = False              # True if operation succeeded
    stdout: str = ""                   # Standard output or result content
    stderr: str = ""                   # Error output if any
    returncode: int = 1                # Exit code (0 = success)
    current_directory: str = os.getcwd()  # Current working directory after operation
```

## 🔧 Development

### Testing the Server

Test the server directly using uvx:

```bash
# Run the server
uvx --from . mcp-terminal

# Test with MCP inspector (if available)
npx @modelcontextprotocol/inspector uvx --from . mcp-terminal
```

### Testing Terminal Functions

Test the terminal functionality directly:

```bash
# Test basic command execution
python -c "
from src.terminal.terminal import terminal_run_command
result = terminal_run_command('echo Hello World')
print(f'Success: {result.success}')
print(f'Output: {result.stdout}')
"

# Test with debug output
python -c "
from src.terminal.terminal import terminal_run_command_and_print
terminal_run_command_and_print('dir' if sys.platform == 'win32' else 'ls -la')
"
```

### Extending the Server

Add new tools to `src/terminal/server.py`:

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

### Architecture Details

- **Entry Point**: `src/terminal/main.py` initializes and runs the FastMCP server
- **Server Logic**: `src/terminal/server.py` defines all MCP tools and manages global state
- **Terminal Engine**: `src/terminal/terminal.py` handles command execution with robust encoding detection
- **Package Script**: Configured in `pyproject.toml` as `mcp-terminal = "terminal.main:main"`

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Encoding errors with international characters** | The system uses multiple encoding detection algorithms - check your locale settings |
| **Permission denied errors** | Ensure the process has necessary permissions for the commands you're running |
| **Command not found** | Verify the command exists in your system PATH |
| **Claude Desktop not connecting** | Check config path is absolute, restart Claude Desktop, verify uvx is in PATH |
| **File not found errors** | File paths are relative to current directory - use absolute paths if needed |
| **Directory creation fails** | Verify parent directory exists and you have write permissions |
| **uvx command fails** | Ensure uv is installed and up to date |

### Getting Help

1. **Check the logs** - Look for error messages in Claude Desktop console
2. **Verify paths** - Ensure all paths in config are absolute and correct
3. **Test manually** - Run `uvx --from . mcp-terminal` to test the server directly
4. **Check permissions** - Verify file and directory permissions
5. **Test encoding** - Use the debug functions to test command execution directly

### Debug Mode

For troubleshooting command execution:

```python
from src.terminal.terminal import terminal_run_command_and_print

# This will print detailed output for debugging
terminal_run_command_and_print("your-command-here")
```

## 🚀 Advanced Configuration

### Custom Environment Variables

Set custom environment variables for the server:

```json
{
  "mcpServers": {
    "Terminal Server": {
      "command": "uvx",
      "args": ["--from", "/path/to/mcp-terminal", "mcp-terminal"],
      "env": {
        "CUSTOM_VAR": "value",
        "PATH": "/custom/path:$PATH"
      }
    }
  }
}
```

### Alternative Installation Methods

If you prefer not to use uvx, you can install dependencies manually:

```bash
# Install with uv
uv sync

# Run with uv directly
uv run python -m terminal.main

# Or install with pip and run with Python
pip install -e .
python -m terminal.main
```

Then update your Claude Desktop config:

```json
{
  "mcpServers": {
    "Terminal Server": {
      "command": "python",
      "args": ["-m", "terminal.main"],
      "cwd": "/absolute/path/to/mcp-terminal"
    }
  }
}
```

### Security Considerations

- Commands run with the same permissions as the MCP server process
- File operations are limited to areas accessible by the user account
- No privilege escalation is performed
- Directory traversal is handled by Python's `os.path.join()` and `os.path.abspath()`
- UTF-8 encoding is enforced for file operations to prevent encoding attacks

## 📝 Changelog

### v1.0.2 (Current)
- ✨ Added comprehensive file operations: `create_file`, `read_file`, `delete_file`
- ✨ Added directory operations: `create_directory`
- ✨ Enhanced directory state management across all operations
- ✨ Improved error handling for file system operations
- ✨ UTF-8 encoding enforcement for file operations
- 🔧 Better path resolution using `os.path.join()` for cross-platform compatibility
- 🔧 Automatic parent directory creation for file operations

### v1.0.1
- ✨ Directory state management with global current_directory tracking
- ✨ Added tools: `change_working_directory`, `get_current_directory`
- ✨ Automatic `cd` command routing to directory change tool
- 🔧 Enhanced command parsing with `shlex.split()`

### v1.0.0 
- ✨ Initial release with FastMCP integration
- ✨ Cross-platform terminal command execution
- ✨ Multi-encoding detection for international character support
- ✨ Structured command results with Pydantic models
- ✨ MCP server integration with Claude Desktop

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/mcp-terminal.git
cd mcp-terminal

# Test the installation
uvx --from . mcp-terminal

# For development with dependencies
uv sync
```

### Code Style

- Follow Python PEP 8 style guidelines
- Use type hints for function parameters and return values
- Document all public functions with comprehensive docstrings
- Handle errors gracefully and return appropriate `command_result` objects
- Use Pydantic models for structured data
- Maintain cross-platform compatibility

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) for the excellent specification
- [Anthropic](https://anthropic.com) for Claude and the MCP ecosystem
- [FastMCP](https://github.com/jlowin/fastmcp) for the lightweight server framework
- [uv](https://docs.astral.sh/uv/) for modern Python package management

---

**Made with ❤️ for the Claude community**

> Have questions or suggestions? Open an issue or start a discussion!