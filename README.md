# MCP Terminal Server

A Model Context Protocol (MCP) server that enables Claude to execute terminal commands safely and retrieve structured results. This bridge allows AI assistants to interact with your local system through a controlled command execution interface.

## Features

- **Secure Command Execution**: Run terminal commands through a structured MCP interface
- **Smart Encoding Detection**: Automatically handles system encoding (including Korean and other non-ASCII characters)
- **Structured Results**: Returns detailed command results with success status, output, errors, and return codes
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Error Handling**: Robust error handling with fallback encoding support

## Installation

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager (recommended)
- Claude Desktop (for MCP integration)

### Setup

1. **Clone or create the project directory:**
   ```bash
   mkdir mcp-terminal
   cd mcp-terminal
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

   Or with pip:
   ```bash
   pip install "mcp[cli]>=1.12.2" "pydantic>=2.11.7"
   ```

3. **Set Python version (if using uv):**
   ```bash
   echo "3.13" > .python-version
   ```

## Configuration

### Claude Desktop Integration

Add the following configuration to your Claude Desktop config file:

**Location:**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "Terminal Server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/mcp-terminal",
        "main.py"
      ]
    }
  }
}
```

> **Note**: Replace `/path/to/your/mcp-terminal` with the actual path to your project directory.

## Usage

### Starting the Server

#### With uv (Recommended)
```bash
uv run main.py
```

#### With Python directly
```bash
python main.py
```

### Using with Claude Desktop

1. Ensure the server is configured in your `claude_desktop_config.json`
2. Restart Claude Desktop
3. Start a new conversation with Claude
4. Claude will automatically have access to the terminal functionality

### Example Commands Through Claude

Once integrated, you can ask Claude to:

```
"Check what files are in the current directory"
"Show me the system information"
"Create a new Python file called hello.py"
"Run my Python script"
"Check the git status of this repository"
```

Claude will execute these commands using the terminal server and provide structured results.

## Project Structure

```
mcp-terminal/
├── main.py                    # Entry point for the MCP server
├── server.py                  # FastMCP server configuration
├── terminal.py                # Core terminal execution logic
├── pyproject.toml            # Project dependencies and metadata
├── claude_desktop_config.json # Claude Desktop configuration
├── .python-version           # Python version specification
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── uv.lock                  # Dependency lock file
├── .venv/                   # Virtual environment (created by uv)
└── __pycache__/            # Python cache files
```

## API Reference

### `run_command_tool(command)`

Executes a terminal command and returns structured results.

**Parameters:**
- `command` (str | list[str]): The command to execute. Can be a string or list of arguments.

**Returns:**
- `command_result`: A Pydantic model with the following fields:
  - `success` (bool): Whether the command executed successfully
  - `stdout` (str): Standard output from the command
  - `stderr` (str): Standard error output from the command
  - `returncode` (int): Exit code of the command

**Example:**
```python
from terminal import run_command

result = run_command("ls -la")
if result.success:
    print(result.stdout)
else:
    print(f"Error: {result.stderr}")
```

## Security Considerations

- **Controlled Execution**: Commands are executed through a structured interface
- **No Privilege Escalation**: Runs with the same permissions as the user
- **Output Sanitization**: Handles encoding and special characters safely
- **Error Containment**: Exceptions are caught and returned as structured errors

> **Warning**: This tool allows command execution on your system. Only use it in trusted environments and be cautious about the commands you allow Claude to execute.

## Development

### Running Tests

```bash
# Test the terminal functionality directly
python -c "from terminal import run_command; print(run_command('echo Hello World'))"
```

### Extending Functionality

To add new tools to the MCP server, modify `server.py`:

```python
@mcp.tool()
def your_new_tool(param: str) -> dict:
    """
    Your new tool description.
    """
    # Implementation here
    return {"result": "success"}
```

## Troubleshooting

### Common Issues

1. **Encoding Errors**: The system automatically detects encoding, but if you encounter issues, check your system's locale settings.

2. **Permission Denied**: Ensure the Python process has the necessary permissions to execute commands.

3. **Command Not Found**: Make sure the commands you're trying to run are available in your system's PATH.

4. **Claude Desktop Not Connecting**: 
   - Verify the path in `claude_desktop_config.json` is correct
   - Restart Claude Desktop after configuration changes
   - Check that uv is installed and accessible from your PATH

### Debug Mode

To debug command execution:

```python
from terminal import run_command_and_print

run_command_and_print("your-command-here")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Feel free to modify and distribute according to your needs.

## Changelog

### v0.1.0
- Initial release
- Basic terminal command execution
- MCP server integration
- Smart encoding detection
- Cross-platform support