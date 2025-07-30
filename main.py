
import subprocess
from pydantic import BaseModel, Field

class command_result(BaseModel):
    success: bool = Field(default=False, description="Indicates if the command was successful")
    stdout: str = Field(default="", description="Standard output of the command")
    stderr: str = Field(default="", description="Standard error output of the command")
    returncode: int = Field(default=-1, description="Return code of the command execution")
    

def run_command(command : list[str] | str) -> command_result:
    try:
        result = subprocess.run(command, 
                                shell=True, 
                                capture_output=True,
                                encoding='utf-8',
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

def run_command_and_print(command : list[str] | str) -> None:
    result = run_command(command)
    if result.success:
        print("Command executed successfully:")
        print(result.stdout)
    else:
        print("Command failed:")
        print(f"Error: {result.stderr} (Return code: {result.returncode})")


def main():
    print("Hello from mcp-terminal!")
    run_command_and_print(['git', '--version'])
    run_command_and_print(['git', '--help'])
    run_command_and_print(['dir'])

if __name__ == "__main__":
    main()
