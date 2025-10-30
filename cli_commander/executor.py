"""Command executor for cli-commander."""

import subprocess
import sys
from typing import Dict, Any


class CommandExecutor:
    """Executes commands defined in the configuration."""
    
    def __init__(self):
        pass
    
    def execute_selector(self, selector_config: Dict[str, Any]) -> int:
        """
        Execute a command from a selector configuration.
        
        Args:
            selector_config: Dictionary containing the selector configuration
            
        Returns:
            Exit code from the executed command
            
        Raises:
            ValueError: If the selector configuration is invalid
        """
        if not isinstance(selector_config, dict):
            raise ValueError("Selector configuration must be a dictionary")
        
        command = selector_config.get("command")
        
        if not command:
            raise ValueError("Selector must have a 'command' field")
        
        description = selector_config.get("description", "")
        
        if description:
            print(f"Running: {description}")
        
        print(f"Command: {command}")
        
        # Execute the command using shell
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=False
            )
            return result.returncode
        except Exception as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            return 1
