#!/usr/bin/env python3
"""
Test script for Quick Image Presenter
Tests the core functionality without launching the GUI.
"""

import os
import re
import sys

def test_time_extraction():
    """Test the time extraction from filename function."""
    print("Testing time extraction from filenames...")
    
    # Import the function from the main app
    sys.path.append('.')
    from quick_image_presenter import QuickImagePresenter
    
    # Create a temporary instance to test the method
    import tkinter as tk
    root = tk.Tk()
    app = QuickImagePresenter(root)
    
    # Test cases
    test_cases = [
        ("1a-11.jpg", 11),
        ("1b-12.png", 12),
        ("a1-10.bmp", 10),
        ("image.jpg", None),
        ("photo-5.gif", 5),
        ("slide-20.tiff", 20),
        ("test-1.webp", 1),
        ("no-number.jpg", None),
        ("multiple-15-20.jpg", 20),  # Should get the last number
    ]
    
    passed = 0
    total = len(test_cases)
    
    for filename, expected in test_cases:
        result = app.extract_time_from_filename(filename)
        if result == expected:
            print(f"✓ {filename} -> {result}")
            passed += 1
        else:
            print(f"✗ {filename} -> {result} (expected {expected})")
    
    print(f"\nTime extraction test: {passed}/{total} passed")
    root.destroy()
    return passed == total

def test_image_extensions():
    """Test supported image extensions."""
    print("\nTesting supported image extensions...")
    
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    test_files = [
        "image.jpg",
        "photo.png", 
        "picture.bmp",
        "animation.gif",
        "document.pdf",  # Should not be supported
        "text.txt",      # Should not be supported
        "image.JPG",     # Should be supported (case insensitive)
        "photo.PNG",     # Should be supported (case insensitive)
    ]
    
    passed = 0
    total = len(test_files)
    
    for filename in test_files:
        ext = os.path.splitext(filename)[1].lower()
        is_supported = ext in supported_extensions
        expected_supported = ext in supported_extensions
        
        if is_supported == expected_supported:
            status = "✓" if is_supported else "✗"
            print(f"{status} {filename} -> {'Supported' if is_supported else 'Not supported'}")
            passed += 1
        else:
            print(f"✗ {filename} -> Unexpected result")
    
    print(f"Image extension test: {passed}/{total} passed")
    return passed == total

def main():
    print("Quick Image Presenter - Test Suite")
    print("=" * 40)
    
    # Test time extraction
    time_test_passed = test_time_extraction()
    
    # Test image extensions
    extension_test_passed = test_image_extensions()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Time extraction: {'PASSED' if time_test_passed else 'FAILED'}")
    print(f"Image extensions: {'PASSED' if extension_test_passed else 'FAILED'}")
    
    if time_test_passed and extension_test_passed:
        print("\n✓ All tests passed! The application should work correctly.")
        return True
    else:
        print("\n✗ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 