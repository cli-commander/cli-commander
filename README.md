# cli-commander

A CLI tool for version controlled aliases inspired by dbt selectors.

## Installation

Install via pip:

```bash
pip install cli-commander
```

Or install from source:

```bash
git clone https://github.com/cli-commander/cli-commander.git
cd cli-commander
pip install -e .
```

## Usage

### Configuration

Create a configuration file named `cli-commander.yml` in either:
- Your current directory (`.`), or
- Your home directory (`~/.cli-commander/`)

The tool will check the local directory first, then fall back to the home directory.

### Configuration Format

```yaml
selectors:
  selector-name:
    description: "Description of what this command does"
    command: "command to execute"
```

### Example Configuration

```yaml
selectors:
  test:
    description: "Run all tests"
    command: "pytest"
  
  build:
    description: "Build the project"
    command: "python setup.py build"
  
  lint:
    description: "Lint code with flake8"
    command: "flake8 ."
```

### Running Commands

Execute a selector using the `cmdr` command:

```bash
cmdr <selector-name>
```

For example:

```bash
cmdr test
cmdr build
cmdr lint
```

### List Available Selectors

To see all available selectors from your configuration:

```bash
cmdr --list <any-selector-name>
```

## License

MIT License - see LICENSE file for details.
