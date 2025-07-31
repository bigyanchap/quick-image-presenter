#!/usr/bin/env python3
"""
Build script for Quick Image Presenter standalone executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0.0"])
    
    try:
        import PIL
        print("✓ Pillow is installed")
    except ImportError:
        print("✗ Pillow not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow>=9.0.0"])

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Clean .spec files
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"Removed {spec_file}")

def build_executable():
    """Build the standalone executable"""
    print("Building standalone executable...")
    
    # Check if icon exists
    icon_flag = ""
    if os.path.exists("icon.png"):
        icon_flag = "--icon=icon.png"
        print("✓ Using icon.png")
    else:
        print("⚠ No icon.png found, using default icon")
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=Quick Image Presenter",
        "--add-data=icon.png;." if os.path.exists("icon.png") else "",
        icon_flag,
        "quick_image_presenter.py"
    ]
    
    # Remove empty strings
    cmd = [arg for arg in cmd if arg]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("✓ Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed with error: {e}")
        return False
    
    return True

def verify_executable():
    """Verify the executable was created"""
    exe_path = None
    
    if sys.platform == "win32":
        exe_path = "dist/Quick Image Presenter.exe"
    else:
        exe_path = "dist/Quick Image Presenter"
    
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        print(f"✓ Executable created: {exe_path}")
        print(f"  Size: {size / (1024*1024):.1f} MB")
        return True
    else:
        print(f"✗ Executable not found at {exe_path}")
        return False

def main():
    """Main build process"""
    print("=" * 50)
    print("Quick Image Presenter - Standalone Build")
    print("=" * 50)
    
    # Check if main file exists
    if not os.path.exists("quick_image_presenter.py"):
        print("✗ quick_image_presenter.py not found!")
        print("Please run this script from the project directory.")
        return 1
    
    # Step 1: Check dependencies
    print("\n1. Checking dependencies...")
    check_dependencies()
    
    # Step 2: Clean previous builds
    print("\n2. Cleaning previous builds...")
    clean_build_dirs()
    
    # Step 3: Build executable
    print("\n3. Building executable...")
    if not build_executable():
        return 1
    
    # Step 4: Verify executable
    print("\n4. Verifying executable...")
    if not verify_executable():
        return 1
    
    print("\n" + "=" * 50)
    print("🎉 Build completed successfully!")
    print("=" * 50)
    print("\nYour executable is ready in the 'dist' folder.")
    print("You can now distribute it to users who don't have Python installed.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 