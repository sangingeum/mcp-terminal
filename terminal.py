import subprocess
import locale
import os
from pydantic import BaseModel, Field

class command_result(BaseModel):
    success: bool = Field(default=False, description="Indicates if the command was successful")
    stdout: str = Field(default="", description="Standard output of the command")
    stderr: str = Field(default="", description="Standard error output of the command")
    returncode: int = Field(default=1, description="Return code of the command execution")
    
def _get_system_encoding():
    """Get the best encoding for the current system"""
    try:
        # Try to get the preferred encoding from locale
        encoding = locale.getpreferredencoding()
        if encoding and encoding.lower() not in ['ascii', 'us-ascii']:
            return encoding
    except:
        pass
    
    # Fallback to UTF-8, which should handle Korean
    return 'utf-8'


def terminal_run_command(command : list[str] | str, cwd : str = os.getcwd()) -> command_result:
    encoding = _get_system_encoding()
    try:
        result = subprocess.run(command, 
                                shell=True, 
                                capture_output=True,
                                encoding=encoding,
                                cwd=cwd,
                                text=True, 
                                errors='replace')
    
        return command_result(
        success = (result.returncode == 0),
        stdout = result.stdout, 
        stderr = result.stderr, 
        returncode = result.returncode    
        )
    
    except Exception as e:
        return command_result()

def terminal_run_command_and_print(command : list[str] | str, cwd : str = os.getcwd()) -> None:
    result = terminal_run_command(command, cwd=cwd)
    if result.success:
        print("Command executed successfully:")
        print(result.stdout)
    else:
        print("Command failed:")
        print(f"Error: {result.stderr} (Return code: {result.returncode})")