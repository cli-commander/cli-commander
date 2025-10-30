"""Tests for the configuration parser."""

import os
import tempfile
import pytest
import yaml
from cli_commander.config import ConfigParser


class TestConfigParser:
    """Test suite for ConfigParser class."""
    
    def test_find_local_config(self):
        """Test finding config file in local directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a local config file
            config_path = os.path.join(tmpdir, "cli-commander.yml")
            with open(config_path, 'w') as f:
                yaml.dump({"selectors": {"test": {"command": "echo test"}}}, f)
            
            # Change to the temp directory
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                parser = ConfigParser()
                found_path = parser.find_config_file()
                assert found_path == config_path
            finally:
                os.chdir(original_dir)
    
    def test_find_home_config(self):
        """Test finding config file in home directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a home directory config
            home_config_dir = os.path.join(tmpdir, ".cli-commander")
            os.makedirs(home_config_dir)
            config_path = os.path.join(home_config_dir, "cli-commander.yml")
            with open(config_path, 'w') as f:
                yaml.dump({"selectors": {"test": {"command": "echo test"}}}, f)
            
            # Use a different temp directory for cwd (no local config)
            with tempfile.TemporaryDirectory() as cwd_dir:
                original_dir = os.getcwd()
                original_home = os.environ.get('HOME')
                try:
                    os.chdir(cwd_dir)
                    os.environ['HOME'] = tmpdir
                    parser = ConfigParser()
                    found_path = parser.find_config_file()
                    assert found_path == config_path
                finally:
                    os.chdir(original_dir)
                    if original_home:
                        os.environ['HOME'] = original_home
                    else:
                        os.environ.pop('HOME', None)
    
    def test_local_config_takes_precedence(self):
        """Test that local config takes precedence over home config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create both local and home configs
            local_config = os.path.join(tmpdir, "cli-commander.yml")
            with open(local_config, 'w') as f:
                yaml.dump({"selectors": {"local": {"command": "echo local"}}}, f)
            
            home_config_dir = os.path.join(tmpdir, "home", ".cli-commander")
            os.makedirs(home_config_dir)
            home_config = os.path.join(home_config_dir, "cli-commander.yml")
            with open(home_config, 'w') as f:
                yaml.dump({"selectors": {"home": {"command": "echo home"}}}, f)
            
            original_dir = os.getcwd()
            original_home = os.environ.get('HOME')
            try:
                os.chdir(tmpdir)
                os.environ['HOME'] = os.path.join(tmpdir, "home")
                parser = ConfigParser()
                found_path = parser.find_config_file()
                assert found_path == local_config
            finally:
                os.chdir(original_dir)
                if original_home:
                    os.environ['HOME'] = original_home
                else:
                    os.environ.pop('HOME', None)
    
    def test_no_config_found(self):
        """Test behavior when no config file is found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                parser = ConfigParser()
                found_path = parser.find_config_file()
                assert found_path is None
            finally:
                os.chdir(original_dir)
    
    def test_load_config(self):
        """Test loading a valid configuration file."""
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
                parser = ConfigParser()
                config = parser.load_config()
                assert config == config_data
                assert parser.config_path == config_path
            finally:
                os.chdir(original_dir)
    
    def test_load_config_not_found(self):
        """Test loading config when no file is found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                parser = ConfigParser()
                with pytest.raises(FileNotFoundError):
                    parser.load_config()
            finally:
                os.chdir(original_dir)
    
    def test_get_selector(self):
        """Test retrieving a selector from config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_data = {
                "selectors": {
                    "test": {
                        "description": "Run tests",
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
                parser = ConfigParser()
                selector = parser.get_selector("test")
                assert selector == config_data["selectors"]["test"]
            finally:
                os.chdir(original_dir)
    
    def test_get_nonexistent_selector(self):
        """Test retrieving a non-existent selector."""
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
                parser = ConfigParser()
                selector = parser.get_selector("nonexistent")
                assert selector is None
            finally:
                os.chdir(original_dir)
    
    def test_empty_config_file(self):
        """Test loading an empty config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "cli-commander.yml")
            with open(config_path, 'w') as f:
                f.write("")
            
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                parser = ConfigParser()
                config = parser.load_config()
                assert config == {}
            finally:
                os.chdir(original_dir)
