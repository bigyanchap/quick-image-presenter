#!/bin/bash

echo "================================================"
echo "Quick Image Presenter - Standalone Build"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi

echo "Python found. Building standalone executable..."
echo

# Run the build script
python3 build_standalone.py

if [ $? -ne 0 ]; then
    echo
    echo "Build failed! Check the error messages above."
    exit 1
fi

echo
echo "Build completed successfully!"
echo "Your executable is in the 'dist' folder."
echo 