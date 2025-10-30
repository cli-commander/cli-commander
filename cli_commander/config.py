"""Configuration file parser for cli-commander."""

import os
import yaml
from typing import Optional, Dict, Any


class ConfigParser:
    """Parses and manages cli-commander configuration files."""
    
    LOCAL_CONFIG_NAME = "cli-commander.yml"
    HOME_CONFIG_DIR = ".cli-commander"
    HOME_CONFIG_NAME = "cli-commander.yml"
    
    def __init__(self):
        self.config: Optional[Dict[str, Any]] = None
        self.config_path: Optional[str] = None
    
    def find_config_file(self) -> Optional[str]:
        """
        Find the configuration file by checking:
        1. ./cli-commander.yml (local directory)
        2. ~/.cli-commander/cli-commander.yml (home directory)
        
        Returns:
            Path to the config file if found, None otherwise
        """
        # Check local directory first
        local_config = os.path.join(os.getcwd(), self.LOCAL_CONFIG_NAME)
        if os.path.isfile(local_config):
            return local_config
        
        # Check home directory
        home_config = os.path.join(
            os.path.expanduser("~"),
            self.HOME_CONFIG_DIR,
            self.HOME_CONFIG_NAME
        )
        if os.path.isfile(home_config):
            return home_config
        
        return None
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load the configuration file.
        
        Returns:
            Parsed configuration as a dictionary
            
        Raises:
            FileNotFoundError: If no configuration file is found
            yaml.YAMLError: If the YAML file is invalid
        """
        config_path = self.find_config_file()
        
        if config_path is None:
            raise FileNotFoundError(
                f"No configuration file found. Please create either:\n"
                f"  - {self.LOCAL_CONFIG_NAME} in the current directory, or\n"
                f"  - ~/{self.HOME_CONFIG_DIR}/{self.HOME_CONFIG_NAME}"
            )
        
        self.config_path = config_path
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        if self.config is None:
            self.config = {}
        
        return self.config
    
    def get_selector(self, selector_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a selector configuration by name.
        
        Args:
            selector_name: Name of the selector to retrieve
            
        Returns:
            Selector configuration dictionary or None if not found
        """
        if self.config is None:
            self.load_config()
        
        selectors = self.config.get("selectors", {})
        return selectors.get(selector_name)
