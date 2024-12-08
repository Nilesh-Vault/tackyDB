#!/usr/bin/env python3
import subprocess
import sys
import os

# Check if Python 3.11 is installed
try:
    subprocess.check_call([sys.executable, "--version"])
except subprocess.CalledProcessError:
    print("Python 3.11 is not installed. Please install Python 3.11 and try again.")
    sys.exit(1)

# Create a virtual environment named 'env' using Python 3.11
venv_path = os.path.join(os.getcwd(), "env")
subprocess.check_call([sys.executable, "-m", "venv", venv_path])

# Activate the virtual environment
if os.name == "nt":  # Windows
    activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
else:  # Unix or MacOS
    activate_script = os.path.join(venv_path, "bin", "activate")

# Install required packages
requirements = ["ruff", "ruff-lsp"]

# Install packages using pip
pip_executable = (
    os.path.join(venv_path, "bin", "pip")
    if os.name != "nt"
    else os.path.join(venv_path, "Scripts", "pip.exe")
)
subprocess.check_call([pip_executable, "install"] + requirements)

# Create a requirements.txt file
with open("requirements.txt", "w") as f:
    subprocess.check_call([pip_executable, "freeze"], stdout=f)

print("Setup complete. Your virtual environment is ready to use.")

print("Setup complete. Your virtual environment is ready to use.")
if os.name == "nt":
    print("To activate the virtual environment, run:")
    print(f"    {activate_script}")
else:
    print("To activate the virtual environment, run:")
    print(f"    source {activate_script}")

# Create Database folder for storing files
try:
    os.mkdir("database")
except Exception as e:
    print(f"Error creating database folder: {e}")