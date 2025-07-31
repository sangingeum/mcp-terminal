# MCP Terminal Server

> A secure Model Context Protocol (MCP) server that bridges Claude AI with your local terminal and file system, enabling safe command execution and file operations through a structured interface.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.12.2+-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](#license)

## ✨ Features

- 🛡️ **Secure Execution** - Commands run with user-level permissions only
- 🌍 **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux
- 🔤 **Smart Encoding** - Handles international characters (Korean, Chinese, etc.)
- 📊 **Structured Results** - Returns detailed command output with status codes
- 🎯 **Directory Tracking** - Maintains current working directory state
- 📁 **File Operations** - Create, read, and delete files directly
- 📂 **Directory Management** - Create directories and navigate file system
- ⚡ **Fast Integration** - Quick setup with Claude Desktop

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** - [Download here](https://python.org/downloads/)
- **uv package manager** - [Install guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Claude Desktop** - [Download here](https://claude.ai/download)

### Installation

1. **Clone and setup the project:**
   ```bash
   git clone <repository-url>
   cd mcp-terminal
   uv sync
   ```

2. **Configure Claude Desktop:**
   
   Edit your Claude Desktop config file:
   
   | Platform | Config Location |
   |----------|----------------|
   | Windows | `%APPDATA%\\Claude\\claude_desktop_config.json` |
   | macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
   | Linux | `~/.config/Claude/claude_desktop_config.json` |

   Add this configuration:
   ```json
   {
     "mcpServers": {
       "Terminal Server": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/absolute/path/to/mcp-terminal",
           "main.py"
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

## 🏗️ Architecture

```
mcp-terminal/
├── 📄 main.py                    # MCP server entry point
├── 🖥️ server.py                  # FastMCP server with tools
├── 🔧 terminal.py                # Command execution engine
├── 📦 pyproject.toml            # Dependencies & metadata
├── ⚙️ claude_desktop_config.json # Claude integration config
├── 🐍 .python-version           # Python version lock
├── 📁 .venv/                   # Virtual environment
└── 📚 README.md                # Documentation
```

## 🔌 API Reference

### Core Tools

#### `run_command(command: str | list[str]) -> command_result`
Executes terminal commands with full output capture. Automatically handles `cd` commands by routing them to `change_working_directory`.

**Parameters:**
- `command`: Command string or list of command parts

**Returns:**
- `command_result` object with execution details

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
Creates a new file with specified content. Automatically creates parent directories if needed.

**Parameters:**
- `file_path`: Path to the file to create (relative to current directory)
- `content`: Content to write to the file

**Returns:**
- `command_result` object with creation status

#### `read_file(file_path: str) -> command_result`
Reads and returns the content of a file.

**Parameters:**
- `file_path`: Path to the file to read (relative to current directory)

**Returns:**
- `command_result` object with file content in stdout

#### `delete_file(file_path: str) -> command_result`
Deletes a specified file.

**Parameters:**
- `file_path`: Path to the file to delete (relative to current directory)

**Returns:**
- `command_result` object with deletion status

### Directory Operations

#### `create_directory(directory_path: str) -> command_result`
Creates a new directory at the specified path.

**Parameters:**
- `directory_path`: Path to the directory to create (relative to current directory)

**Returns:**
- `command_result` object with creation status

### Response Format

All tools return a `command_result` object with the following structure:

```python
{
    "success": bool,              # True if operation succeeded
    "stdout": str,                # Standard output or result content
    "stderr": str,                # Error output if any
    "returncode": int,            # Exit code (0 = success)
    "current_directory": str      # Current working directory after operation
}
```

## 🔧 Development

### Running Tests

Test the terminal functionality directly:

```bash
# Basic functionality test
python -c "from terminal import terminal_run_command; print(terminal_run_command('echo Hello World'))"

# Interactive testing
python -c "from terminal import terminal_run_command_and_print; terminal_run_command_and_print('ls -la')"
```

### Testing MCP Server

Test the server directly:

```bash
# Run the server
uv run main.py

# Test with MCP inspector (if available)
npx @modelcontextprotocol/inspector uv run main.py
```

### Extending the Server

Add new tools to `server.py`:

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

### Debug Mode

For troubleshooting command execution:

```python
from terminal import terminal_run_command_and_print

# This will print detailed output for debugging
terminal_run_command_and_print("your-command-here")
```

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Encoding errors with international characters** | System automatically detects encoding, but verify your locale settings |
| **Permission denied errors** | Ensure Python has necessary permissions for the commands you're running |
| **Command not found** | Verify the command exists in your system PATH |
| **Claude Desktop not connecting** | Check config path is absolute, restart Claude Desktop, verify uv is in PATH |
| **File not found errors** | Check file paths are relative to current directory or use absolute paths |
| **Directory creation fails** | Verify parent directory exists and you have write permissions |

### Getting Help

1. **Check the logs** - Look for error messages in Claude Desktop console
2. **Verify paths** - Ensure all paths in config are absolute and correct
3. **Test manually** - Run `uv run main.py` to test the server directly
4. **Check permissions** - Verify file and directory permissions
5. **Test file operations** - Use the debug functions to test file operations directly

## 🚀 Advanced Configuration

### Custom Python Installation

If not using uv, modify the Claude Desktop config:

```json
{
  "mcpServers": {
    "Terminal Server": {
      "command": "python",
      "args": ["/absolute/path/to/mcp-terminal/main.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/mcp-terminal"
      }
    }
  }
}
```

### Environment Variables

Set custom environment variables for the server:

```json
{
  "mcpServers": {
    "Terminal Server": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mcp-terminal", "main.py"],
      "env": {
        "CUSTOM_VAR": "value",
        "PATH": "/custom/path:$PATH"
      }
    }
  }
}
```

### Security Considerations

- Commands run with the same permissions as the MCP server process
- File operations are limited to areas accessible by the user account
- No privilege escalation is performed
- Directory traversal is handled by Python's path resolution

## 📝 Changelog

### v1.0.2 (Current)
- ✨ Added file operations: `create_file`, `read_file`, `delete_file`
- ✨ Added directory operations: `create_directory`
- ✨ Enhanced directory state management across all operations
- ✨ Improved error handling for file system operations
- 🔧 Better path resolution for relative paths

### v1.0.1
- ✨ Directory state management
- ✨ Added tools: `change_directory`, `get_current_directory`
- ✨ Renamed tool: `run_command_tools` → `run_command`

### v1.0.0 
- ✨ Initial release
- ✨ Cross-platform terminal command execution
- ✨ MCP server integration with Claude Desktop
- ✨ Smart encoding detection for international characters

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

# Setup development environment
uv sync --dev

# Run tests (when available)
uv run pytest
```

### Code Style

- Follow Python PEP 8 style guidelines
- Use type hints for function parameters and return values
- Document all public functions with docstrings
- Handle errors gracefully and return appropriate `command_result` objects

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) for the excellent specification
- [Anthropic](https://anthropic.com) for Claude and the MCP ecosystem
- [FastMCP](https://github.com/jlowin/fastmcp) for the server framework

---

**Made with ❤️ for the Claude community**

> Have questions or suggestions? Open an issue or start a discussion!