#!/usr/bin/env python3
"""
Build script to create executable files for all opponent types
"""

import os
import sys
import subprocess
import shutil

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")
EXE_DIR = os.path.join(PROJECT_ROOT, "exe_builds")

# Ensure exe directory exists
os.makedirs(EXE_DIR, exist_ok=True)

def get_python_executable():
    """Get the Python executable path"""
    return "C:/Users/patss/AppData/Local/Programs/Python/Python313/python.exe"

def build_executable(script_name, output_name, is_uci=False):
    """Build a single executable"""
    print(f"Building {output_name}...")
    
    if is_uci:
        script_path = os.path.join(SRC_DIR, script_name)
    else:
        script_path = os.path.join(BUILD_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"Warning: {script_path} not found, skipping...")
        return False
    
    output_path = os.path.join(EXE_DIR, output_name)
    
    cmd = [
        get_python_executable(),
        "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--distpath", EXE_DIR,
        "--workpath", os.path.join(PROJECT_ROOT, "temp_build"),
        "--specpath", os.path.join(PROJECT_ROOT, "temp_build"),
        "--name", output_name,
        script_path
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)
        print(f"Successfully built {output_name}.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to build {output_name}: {e}")
        return False

def create_uci_executables():
    """Create UCI executables for each opponent type"""
    opponent_types = [
        ("opening_only_random", "OpponentEngine_Opening_Random"),
        ("random_only", "OpponentEngine_Random_Only"),
        ("elo_400", "OpponentEngine_400_ELO"),
        ("opening_plus_elo_800", "OpponentEngine_Opening_800_ELO"),
        ("opening_plus_elo_1200", "OpponentEngine_Opening_1200_ELO")
    ]
    
    # Create wrapper scripts for each opponent type
    for opponent_type, exe_name in opponent_types:
        wrapper_content = f'''#!/usr/bin/env python3
"""
UCI Wrapper for {exe_name}
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from uci_interface import UCIOpponentEngine, OpponentType

if __name__ == "__main__":
    uci_engine = UCIOpponentEngine(OpponentType("{opponent_type}"))
    uci_engine.run()
'''
        
        wrapper_path = os.path.join(BUILD_DIR, f"uci_{opponent_type}.py")
        with open(wrapper_path, 'w') as f:
            f.write(wrapper_content)
        
        # Build the executable
        build_executable(f"uci_{opponent_type}.py", exe_name, is_uci=False)

def main():
    """Main build function"""
    print("Building Opponent Engine Executables")
    print("=" * 50)
    
    # Check if PyInstaller is available
    try:
        subprocess.run([get_python_executable(), "-c", "import PyInstaller"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("PyInstaller not found. Installing...")
        subprocess.run([get_python_executable(), "-m", "pip", "install", "pyinstaller"], 
                      check=True)
    
    # Build interactive versions
    print("\nBuilding interactive versions...")
    build_executable("opening_random_opponent.py", "Interactive_Opening_Random", is_uci=False)
    build_executable("random_only_opponent.py", "Interactive_Random_Only", is_uci=False)
    build_executable("elo_400_opponent.py", "Interactive_400_ELO", is_uci=False)
    build_executable("opening_elo_800_opponent.py", "Interactive_Opening_800_ELO", is_uci=False)
    build_executable("opening_elo_1200_opponent.py", "Interactive_Opening_1200_ELO", is_uci=False)
    
    # Build UCI versions for tournament play
    print("\nBuilding UCI tournament versions...")
    create_uci_executables()
    
    # Clean up temporary files
    temp_build_dir = os.path.join(PROJECT_ROOT, "temp_build")
    if os.path.exists(temp_build_dir):
        shutil.rmtree(temp_build_dir)
    
    print(f"\nBuild complete! Executables are in: {EXE_DIR}")
    print("\nAvailable executables:")
    print("Interactive versions (for testing):")
    print("  - Interactive_Opening_Random.exe")
    print("  - Interactive_Random_Only.exe") 
    print("  - Interactive_400_ELO.exe")
    print("  - Interactive_Opening_800_ELO.exe")
    print("  - Interactive_Opening_1200_ELO.exe")
    print("\nUCI versions (for tournament play):")
    print("  - OpponentEngine_Opening_Random.exe")
    print("  - OpponentEngine_Random_Only.exe")
    print("  - OpponentEngine_400_ELO.exe")
    print("  - OpponentEngine_Opening_800_ELO.exe")
    print("  - OpponentEngine_Opening_1200_ELO.exe")

if __name__ == "__main__":
    main()
