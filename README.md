# MCP Terminal Server

> A secure Model Context Protocol (MCP) server that bridges Claude AI with your local terminal, enabling safe command execution through a structured interface.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/MCP-1.12.2+-green.svg)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/license-Open%20Source-brightgreen.svg)](#license)

## ✨ Features

- 🛡️ **Secure Execution** - Commands run with user-level permissions only
- 🌍 **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux
- 🔤 **Smart Encoding** - Handles international characters (Korean, Chinese, etc.)
- 📊 **Structured Results** - Returns detailed command output with status codes
- 🎯 **Directory Tracking** - Maintains current working directory state
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
   | Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
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
   - Claude now has terminal access! 🎉

## 💡 Usage Examples

Once integrated, you can interact with your terminal through Claude naturally:

```
You: "What files are in my current directory?"
Claude: [Executes `ls` or `dir` and shows results]

You: "Create a Python file that prints 'Hello World'"
Claude: [Creates the file using appropriate commands]

You: "Show me the git status of this repository"
Claude: [Runs `git status` and explains the output]

You: "Navigate to my Documents folder and list the contents"
Claude: [Changes directory and lists files]
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
Executes terminal commands with full output capture.

**Example:**
```python
# Through Claude: "Run the command 'python --version'"
# Returns structured result with stdout, stderr, and return code
```

#### `change_directory(path: str) -> command_result`
Changes the current working directory with state persistence.

**Example:**
```python
# Through Claude: "Navigate to the src folder"
# Updates internal directory state
```

#### `get_current_directory() -> str`
Returns the current working directory path.

### Response Format

All commands return a `command_result` object:

```python
{
    "success": bool,      # True if command succeeded
    "stdout": str,        # Standard output
    "stderr": str,        # Error output  
    "returncode": int     # Exit code (0 = success)
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

### Extending the Server

Add new tools to `server.py`:

```python
@mcp.tool()
def my_custom_tool(param: str) -> dict:
    """
    Description of your custom tool.
    
    Args:
        param: Parameter description
        
    Returns:
        dict: Result description
    """
    # Your implementation here
    return {"result": "success"}
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

### Getting Help

1. **Check the logs** - Look for error messages in Claude Desktop console
2. **Verify paths** - Ensure all paths in config are absolute and correct
3. **Test manually** - Run `uv run main.py` to test the server directly
4. **Check permissions** - Verify file and directory permissions

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

## 📝 Changelog

### v1.0.1 (Current)
- ✨ Directory state management
- ✨ Added tools: ```change_directory```, ```get_current_directory```
- ✨ Renamed a tool: ```run_command_tools``` -> ```run_command```

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

# Run tests
uv run pytest  # (when tests are added)
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io) for the excellent specification
- [Anthropic](https://anthropic.com) for Claude and the MCP ecosystem
- [FastMCP](https://github.com/jlowin/fastmcp) for the server framework

---

**Made with ❤️ for the Claude community**

> Have questions or suggestions? Open an issue or start a discussion!