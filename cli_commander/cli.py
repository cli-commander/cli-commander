"""Command-line interface for cli-commander."""

import sys
import argparse
from cli_commander.config import ConfigParser
from cli_commander.executor import CommandExecutor


def main():
    """Main entry point for the cmdr command."""
    parser = argparse.ArgumentParser(
        prog="cmdr",
        description="A CLI tool for version controlled aliases inspired by dbt selectors"
    )
    
    parser.add_argument(
        "selector",
        nargs="?",
        help="Name of the selector to execute from the configuration file"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available selectors"
    )
    
    args = parser.parse_args()
    
    # Initialize config parser
    config_parser = ConfigParser()
    
    try:
        config = config_parser.load_config()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Handle --list flag
    if args.list:
        selectors = config.get("selectors", {})
        if not selectors:
            print("No selectors defined in configuration file")
            sys.exit(0)
        
        print(f"Available selectors from {config_parser.config_path}:")
        for name, selector_config in selectors.items():
            description = selector_config.get("description", "") if isinstance(selector_config, dict) else ""
            if description:
                print(f"  {name}: {description}")
            else:
                print(f"  {name}")
        sys.exit(0)
    
    # Check if selector argument is provided
    if not args.selector:
        print("Error: Selector name is required", file=sys.stderr)
        print("\nUse 'cmdr --list' to see available selectors", file=sys.stderr)
        sys.exit(1)
    
    # Get the selector
    selector_config = config_parser.get_selector(args.selector)
    
    if selector_config is None:
        print(f"Error: Selector '{args.selector}' not found in configuration", file=sys.stderr)
        print(f"\nAvailable selectors:", file=sys.stderr)
        selectors = config.get("selectors", {})
        for name in selectors.keys():
            print(f"  {name}", file=sys.stderr)
        sys.exit(1)
    
    # Execute the command
    executor = CommandExecutor()
    
    try:
        exit_code = executor.execute_selector(selector_config)
        sys.exit(exit_code)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing selector: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
