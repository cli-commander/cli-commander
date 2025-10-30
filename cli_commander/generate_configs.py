import os
import sys
from pathlib import Path

CONFIG_CONTENT = """# Example cli-commander configuration file
# Place this file in your project root as cli-commander.yml
# or in your home directory as ~/.cli-commander/cli-commander.yml

# selectors:
#   name:
#       description:
#       command:
#   name:
# etc.
"""

def create_config_file(target: Path):
    """Create the config file if it doesn't already exist."""
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(CONFIG_CONTENT)
        print(f"Created configuration file at {target}")
    else:
        print(f"Configuration file already exists at {target}")

def main():
    # 1. Install directory path (where the package itself lives)
    install_dir = Path(__file__).resolve().parent
    project_config = install_dir / "cli-commander.yml"
    create_config_file(project_config)

    # 2. User home directory config (~/.cli-commander/cli-commander.yml)
    home_config_dir = Path.home() / ".cli-commander"
    home_config_file = home_config_dir / "cli-commander.yml"
    create_config_file(home_config_file)


if __name__ == "__main__":
    main()