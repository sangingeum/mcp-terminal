import subprocess
import os
import locale
import sys
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

    # First try with the detected encoding
    result = subprocess.run(command, 
                            shell=True, 
                            capture_output=True,
                            cwd=cwd,
                            text=False)  # Get bytes first

    # Decode the output properly
    stdout = _decode_output(result.stdout, encodings)
    stderr = _decode_output(result.stderr, encodings)
    success = (result.returncode == 0)
    
    if change_directory and success:
        path = command[1] if isinstance(command, list) and len(command) > 1 else command[3:] if isinstance(command, str) and command.startswith("cd ") else ""
        cwd = os.path.abspath(os.path.join(cwd, path))
    
    return command_result(
        success = success,
        stdout = stdout, 
        stderr = stderr, 
        returncode = result.returncode,
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