#!/usr/bin/env python3
"""
Quick Image Presenter Launcher
A simple launcher script for the Quick Image Presenter application.
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import tkinter
        print("✓ Tkinter is available")
    except ImportError:
        print("✗ Tkinter is not available. Please install Python with Tkinter support.")
        return False
    
    try:
        from PIL import Image, ImageTk
        print("✓ Pillow is available")
    except ImportError:
        print("✗ Pillow is not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow>=10.0.0"])
            print("✓ Pillow installed successfully")
        except subprocess.CalledProcessError:
            print("✗ Failed to install Pillow. Please install manually: pip install Pillow")
            return False
    
    return True

def main():
    print("Quick Image Presenter Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease resolve the dependency issues and try again.")
        input("Press Enter to exit...")
        return
    
    print("\nStarting Quick Image Presenter...")
    print("=" * 40)
    
    try:
        # Import and run the main application
        from quick_image_presenter import main as run_app
        run_app()
    except ImportError as e:
        print(f"Error importing application: {e}")
        print("Make sure quick_image_presenter.py is in the same directory.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Error running application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 