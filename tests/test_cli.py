"""Tests for the CLI interface."""

import os
import sys
import tempfile
import yaml
import pytest
from cli_commander.cli import main


class TestCLI:
    """Test suite for CLI interface."""
    
    def test_list_selectors(self, capsys, monkeypatch):
        """Test listing available selectors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_data = {
                "selectors": {
                    "test": {
                        "description": "Run tests",
                        "command": "pytest"
                    },
                    "build": {
                        "command": "make build"
                    }
                }
            }
            config_path = os.path.join(tmpdir, "cli-commander.yml")
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f)
            
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                monkeypatch.setattr(sys, 'argv', ['cmdr', '--list', 'test'])
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0
                
                captured = capsys.readouterr()
                assert "test:" in captured.out or "test" in captured.out
                assert "build" in captured.out
            finally:
                os.chdir(original_dir)
    
    def test_selector_not_found(self, capsys, monkeypatch):
        """Test error when selector is not found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_data = {
                "selectors": {
                    "test": {
                        "command": "pytest"
                    }
                }
            }
            config_path = os.path.join(tmpdir, "cli-commander.yml")
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f)
            
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                monkeypatch.setattr(sys, 'argv', ['cmdr', 'nonexistent'])
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                
                captured = capsys.readouterr()
                assert "not found" in captured.err
            finally:
                os.chdir(original_dir)
    
    def test_no_config_file(self, capsys, monkeypatch):
        """Test error when no config file is found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                monkeypatch.setattr(sys, 'argv', ['cmdr', 'test'])
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                
                captured = capsys.readouterr()
                assert "No configuration file found" in captured.err
            finally:
                os.chdir(original_dir)
    
    def test_execute_selector(self, monkeypatch):
        """Test executing a selector."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_data = {
                "selectors": {
                    "test": {
                        "command": "echo 'success'",
                        "description": "Test command"
                    }
                }
            }
            config_path = os.path.join(tmpdir, "cli-commander.yml")
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f)
            
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                monkeypatch.setattr(sys, 'argv', ['cmdr', 'test'])
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0
            finally:
                os.chdir(original_dir)
