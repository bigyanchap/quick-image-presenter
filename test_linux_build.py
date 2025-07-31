#!/usr/bin/env python3
"""
Test script to verify Linux compatibility for Quick Image Presenter
"""

import sys
import platform

def test_dependencies():
    """Test if all required dependencies are available"""
    print("Testing Linux compatibility...")
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    print()
    
    # Test tkinter
    try:
        import tkinter
        print("✅ tkinter - Available")
    except ImportError:
        print("❌ tkinter - Not available")
        print("   Install with: sudo apt-get install python3-tk")
        return False
    
    # Test PIL/Pillow
    try:
        from PIL import Image, ImageTk
        print("✅ PIL/Pillow - Available")
    except ImportError:
        print("❌ PIL/Pillow - Not available")
        print("   Install with: pip install Pillow")
        return False
    
    # Test other required modules
    required_modules = ['os', 're', 'time', 'threading', 'math']
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"❌ {module} - Not available")
            return False
    
    return True

def test_gui_functionality():
    """Test basic GUI functionality"""
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Create a test window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test basic widgets
        frame = ttk.Frame(root)
        label = ttk.Label(frame, text="Test")
        button = ttk.Button(frame, text="Test")
        
        print("✅ GUI functionality - Working")
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ GUI functionality - Error: {e}")
        return False

def test_image_processing():
    """Test image processing functionality"""
    try:
        from PIL import Image, ImageTk
        
        # Create a test image
        test_image = Image.new('RGB', (100, 100), color='red')
        
        # Test image operations
        resized = test_image.resize((50, 50))
        rotated = test_image.rotate(90)
        
        print("✅ Image processing - Working")
        return True
        
    except Exception as e:
        print(f"❌ Image processing - Error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Quick Image Presenter - Linux Compatibility Test")
    print("=" * 50)
    print()
    
    all_tests_passed = True
    
    # Test dependencies
    if not test_dependencies():
        all_tests_passed = False
    
    print()
    
    # Test GUI functionality
    if not test_gui_functionality():
        all_tests_passed = False
    
    print()
    
    # Test image processing
    if not test_image_processing():
        all_tests_passed = False
    
    print()
    print("=" * 50)
    
    if all_tests_passed:
        print("🎉 All tests passed! Linux build should work.")
        print("You can now run: ./build_linux.sh")
    else:
        print("❌ Some tests failed. Please install missing dependencies.")
        print("See Linux_Build_Guide.md for detailed instructions.")
    
    print("=" * 50)

if __name__ == "__main__":
    main() 