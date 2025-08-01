import subprocess
import os
import locale
import sys
import shlex 
from pydantic import BaseModel, Field

class command_result(BaseModel):
    success: bool = Field(default=False, description="Indicates if the command was successful")
    stdout: str = Field(default="", description="Standard output of the command")
    stderr: str = Field(default="", description="Standard error output of the command")
    returncode: int = Field(default=1, description="Return code of the command execution")
    current_directory: str = Field(default=os.getcwd(), description="Current working directory after command execution")

def _get_encoding_candidates() -> list[str]:
    return [sys.stdout.encoding, sys.stdin.encoding, locale.getpreferredencoding()]

def _decode_output(output_bytes, encoding_candidates : list[str] = [] ):
    """Try to decode output with multiple encodings"""
    if isinstance(output_bytes, str):
        return output_bytes
             
    encodings_to_try_last = [
        'utf-8',
        'utf-16',
        'latin1',  # This rarely fails but may produce garbage
    ]
    
    encoding_candidates.extend(encodings_to_try_last)
    
    for encoding in encoding_candidates:
        try:
            return output_bytes.decode(encoding)
        except (UnicodeDecodeError, UnicodeError, LookupError):
            continue
    
    # Last resort: decode with errors='replace'
    try:
        return output_bytes.decode('utf-8', errors='replace')
    except:
        return str(output_bytes)

def terminal_run_command(command : list[str] | str, cwd : str = os.getcwd(), change_directory : bool = False) -> command_result:
    encodings = _get_encoding_candidates()
    try:

        command = command if isinstance(command, list) else shlex.split(command)
        command_str = ' '.join(part for part in command)
        
        if sys.platform == "win32":
            command_str = "powershell -Command " + command_str
        
        result = subprocess.run(command_str, 
                                shell=True,
                                env=os.environ,
                                stdin=subprocess.DEVNULL,
                                check=False,
                                capture_output=True,
                                #executable="powershell" if sys.platform == "win32" else "/bin/bash",
                                cwd=cwd,
                                text=False)

        # Decode the output properly
        stdout = _decode_output(result.stdout, encodings)
        stderr = _decode_output(result.stderr, encodings)
        success = (result.returncode == 0)
        
        if change_directory and success:
            path = command[1] if len(command) > 1 else ""
            cwd = os.path.abspath(os.path.join(cwd, path))

        return command_result(
            success = success,
            stdout = stdout, 
            stderr = stderr, 
            returncode = result.returncode,
            current_directory = cwd
        )
    except Exception as e:
        return command_result(
            success = False,
            stdout = "",
            stderr = str(e),
            returncode = 1,
            current_directory = cwd
        )

def terminal_run_command_and_print(command : list[str] | str, cwd : str = os.getcwd()) -> None:
    result = terminal_run_command(command, cwd=cwd)
    if result.success:
        print("Command executed successfully:")
        print(result.stdout)
    else:
        print("Command failed:")
        print(f"Error: {result.stderr} (Return code: {result.returncode})")