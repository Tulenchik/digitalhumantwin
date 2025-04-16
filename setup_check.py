#!/usr/bin/env python
"""
Setup Check Script for NeuroSync Player

This script checks for all required dependencies and system configurations
needed to run NeuroSync Player properly.
"""

import os
import sys
import importlib.util
import subprocess
import platform

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_module(module_name, package_name=None):
    """Check if a Python module is installed."""
    if package_name is None:
        package_name = module_name
    
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {module_name} is NOT installed. Install with: pip install {package_name}")
        return False
    else:
        print(f"✓ {module_name} is installed")
        return True

def check_command(command, name=None):
    """Check if a command is available on the system."""
    if name is None:
        name = command
    
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✓ {name} is installed")
        return True
    except FileNotFoundError:
        print(f"❌ {name} is NOT installed")
        return False

def check_directory_structure():
    """Check if the directory structure is correct."""
    required_dirs = [
        "utils",
        "utils/stt",
        "utils/tts",
        "utils/llm",
        "utils/audio",
        "utils/vector_db",
        "livelink",
        "livelink/animations",
        "livelink/connect"
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.isdir(directory):
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"❌ Some required directories are missing: {', '.join(missing_dirs)}")
        return False
    else:
        print("✓ Directory structure is correct")
        return True

def check_init_files():
    """Check if __init__.py files exist in all required directories."""
    required_inits = [
        "utils/__init__.py",
        "utils/stt/__init__.py",
        "utils/tts/__init__.py",
        "utils/llm/__init__.py",
        "utils/audio/__init__.py",
        "utils/vector_db/__init__.py",
        "livelink/__init__.py",
        "livelink/animations/__init__.py",
        "livelink/connect/__init__.py"
    ]
    
    missing_inits = []
    for init_file in required_inits:
        if not os.path.isfile(init_file):
            missing_inits.append(init_file)
    
    if missing_inits:
        print(f"❌ Some required __init__.py files are missing: {', '.join(missing_inits)}")
        # Create missing __init__.py files
        for init_file in missing_inits:
            os.makedirs(os.path.dirname(init_file), exist_ok=True)
            with open(init_file, 'w') as f:
                f.write("# This file is intentionally empty to make the directory a proper Python package.\n")
            print(f"  Created {init_file}")
        print("✓ Created missing __init__.py files")
    else:
        print("✓ All required __init__.py files exist")
    
    return True

def main():
    """Main function to check setup requirements."""
    print_header("NeuroSync Player Setup Check")
    
    print(f"Python version: {platform.python_version()}")
    print(f"Operating System: {platform.system()} {platform.release()}")
    
    # Check directory structure and init files
    print_header("Checking Directory Structure")
    check_directory_structure()
    check_init_files()
    
    # Check required core modules
    print_header("Checking Core Dependencies")
    core_modules = [
        ("pygame", "pygame"),
        ("keyboard", "keyboard"),
        ("requests", "requests"),
        ("numpy", "numpy"),
        ("soundfile", "soundfile"),
        ("pydub", "pydub"),
        ("flask", "flask")
    ]
    
    for module, package in core_modules:
        check_module(module, package)
    
    # Check TTS modules
    print_header("Checking TTS Dependencies")
    check_module("kokoro", "kokoro>=0.8.2")
    
    # Check STT modules
    print_header("Checking STT Dependencies")
    whisper_available = check_module("faster_whisper", "faster-whisper")
    
    # Check LLM modules
    print_header("Checking LLM Dependencies")
    check_module("openai", "openai")
    
    # Check for Ollama
    print_header("Checking External Dependencies")
    ollama_available = check_command("ollama")
    
    # Check for ffmpeg
    ffmpeg_available = check_command("ffmpeg")
    
    # Summary and recommendations
    print_header("Summary")
    
    if not whisper_available:
        print("- Install faster-whisper for local speech recognition:")
        print("  pip install faster-whisper")
    
    if not ollama_available:
        print("- Install Ollama for local LLM support:")
        print("  Visit https://ollama.com/ to download and install")
        print("  After installation, pull a model: ollama pull llama3.1:8b")
    
    if not ffmpeg_available:
        print("- Install ffmpeg for audio processing:")
        if platform.system() == "Windows":
            print("  Download from https://ffmpeg.org/download.html or install via Chocolatey:")
            print("  choco install ffmpeg")
        elif platform.system() == "Darwin":  # macOS
            print("  Install with Homebrew: brew install ffmpeg")
        else:  # Linux
            print("  sudo apt-get install ffmpeg  # Debian/Ubuntu")
            print("  sudo yum install ffmpeg      # CentOS/RHEL")
    
    print("\nTo run NeuroSync Player:")
    print("  python llm_to_face.py")

if __name__ == "__main__":
    main() 