from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cli-commander",
    version="0.1.0",
    author="cli-commander",
    description="A CLI tool for version controlled aliases inspired by dbt selectors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cli-commander/cli-commander",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyYAML>=5.1",
    ],
    entry_points={
        "console_scripts": [
            "cmdr=cli_commander.cli:main",
        ],
    },
)
