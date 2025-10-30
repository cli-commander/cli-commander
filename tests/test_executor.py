"""Tests for the command executor."""

import pytest
from cli_commander.executor import CommandExecutor


class TestCommandExecutor:
    """Test suite for CommandExecutor class."""
    
    def test_execute_simple_command(self):
        """Test executing a simple command."""
        executor = CommandExecutor()
        selector_config = {
            "command": "echo 'test'",
            "description": "Echo test"
        }
        exit_code = executor.execute_selector(selector_config)
        assert exit_code == 0
    
    def test_execute_command_without_description(self):
        """Test executing a command without description."""
        executor = CommandExecutor()
        selector_config = {
            "command": "echo 'test'"
        }
        exit_code = executor.execute_selector(selector_config)
        assert exit_code == 0
    
    def test_execute_failing_command(self):
        """Test executing a command that fails."""
        executor = CommandExecutor()
        selector_config = {
            "command": "exit 1"
        }
        exit_code = executor.execute_selector(selector_config)
        assert exit_code == 1
    
    def test_execute_command_with_success_exit_code(self):
        """Test executing a command that succeeds."""
        executor = CommandExecutor()
        selector_config = {
            "command": "exit 0"
        }
        exit_code = executor.execute_selector(selector_config)
        assert exit_code == 0
    
    def test_invalid_selector_config_not_dict(self):
        """Test that non-dict selector config raises ValueError."""
        executor = CommandExecutor()
        with pytest.raises(ValueError, match="Selector configuration must be a dictionary"):
            executor.execute_selector("not a dict")
    
    def test_missing_command_field(self):
        """Test that missing command field raises ValueError."""
        executor = CommandExecutor()
        selector_config = {
            "description": "No command here"
        }
        with pytest.raises(ValueError, match="Selector must have a 'command' field"):
            executor.execute_selector(selector_config)
    
    def test_empty_command_field(self):
        """Test that empty command field raises ValueError."""
        executor = CommandExecutor()
        selector_config = {
            "command": ""
        }
        with pytest.raises(ValueError, match="Selector must have a 'command' field"):
            executor.execute_selector(selector_config)
