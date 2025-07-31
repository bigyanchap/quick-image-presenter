#!/bin/bash

echo "================================================"
echo "Quick Image Presenter - Linux Standalone Build"
echo "================================================"
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ and try again"
    echo "Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip3 and try again"
    exit 1
fi

echo "Python 3 found. Setting up Linux build environment..."
echo

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist __pycache__ *.spec

# Build the executable
echo "Building Linux standalone executable..."
python -m PyInstaller \
    --onefile \
    --windowed \
    --icon=icon.png \
    --name="Quick Image Presenter" \
    --add-data="icon.png:." \
    quick_image_presenter.py

# Check if build was successful
if [ -f "dist/Quick Image Presenter" ]; then
    echo
    echo "✅ Build completed successfully!"
    echo "📁 Executable location: dist/Quick Image Presenter"
    echo "📏 Size: $(du -h dist/Quick\ Image\ Presenter | cut -f1)"
    echo
    echo "🚀 To run the application:"
    echo "   ./dist/Quick\ Image\ Presenter"
    echo
    echo "📋 To make it executable:"
    echo "   chmod +x dist/Quick\ Image\ Presenter"
    echo
    echo "📦 To distribute:"
    echo "   - Copy the executable to any Linux system"
    echo "   - Make sure the target system has required libraries"
    echo "   - Run: chmod +x 'Quick Image Presenter'"
else
    echo
    echo "❌ Build failed! Check the error messages above."
    exit 1
fi 