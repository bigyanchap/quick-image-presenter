#!/usr/bin/env python3
"""
Cross-platform Linux build script for Quick Image Presenter
This script can be run on Windows to create a Linux executable
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker not found")
        return False

def check_wsl():
    """Check if WSL is available"""
    try:
        result = subprocess.run(['wsl', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ WSL found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ WSL not found")
        return False

def build_with_docker():
    """Build Linux executable using Docker"""
    print("\n🐳 Building with Docker...")
    
    # Create Dockerfile for building
    dockerfile_content = """FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    python3 \\
    python3-pip \\
    python3-venv \\
    python3-dev \\
    python3-tk \\
    tk-dev \\
    libjpeg-dev \\
    libpng-dev \\
    libtiff-dev \\
    libwebp-dev \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy application files
COPY quick_image_presenter.py .
COPY icon.png .

# Build the executable
RUN python3 -m PyInstaller \\
    --onefile \\
    --windowed \\
    --icon=icon.png \\
    --name="Quick Image Presenter" \\
    --add-data="icon.png:." \\
    quick_image_presenter.py

# Create output directory
RUN mkdir -p /output

# Copy the executable to output
RUN cp dist/"Quick Image Presenter" /output/
RUN chmod +x /output/"Quick Image Presenter"

# Set the output as volume
VOLUME /output
"""
    
    with open('Dockerfile.linux', 'w') as f:
        f.write(dockerfile_content)
    
    try:
        # Build Docker image
        print("Building Docker image...")
        subprocess.run(['docker', 'build', '-f', 'Dockerfile.linux', '-t', 'quick-image-presenter-linux', '.'], 
                      check=True)
        
        # Run container and copy executable
        print("Extracting executable...")
        container_name = "quick-image-presenter-build"
        
        # Remove existing container if it exists
        subprocess.run(['docker', 'rm', '-f', container_name], 
                      capture_output=True, check=False)
        
        # Run container
        subprocess.run(['docker', 'run', '--name', container_name, 'quick-image-presenter-linux'], 
                      check=True)
        
        # Create dist directory if it doesn't exist
        os.makedirs('dist', exist_ok=True)
        
        # Copy executable from container
        subprocess.run(['docker', 'cp', f'{container_name}:/output/Quick Image Presenter', 'dist/'], 
                      check=True)
        
        # Clean up container
        subprocess.run(['docker', 'rm', container_name], check=True)
        
        print("✅ Linux executable created successfully!")
        print(f"📁 Location: dist/Quick Image Presenter")
        
        # Get file size
        if os.path.exists('dist/Quick Image Presenter'):
            size = os.path.getsize('dist/Quick Image Presenter')
            print(f"📏 Size: {size / (1024*1024):.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker build failed: {e}")
        return False
    finally:
        # Clean up Dockerfile
        if os.path.exists('Dockerfile.linux'):
            os.remove('Dockerfile.linux')

def build_with_wsl():
    """Build Linux executable using WSL"""
    print("\n🐧 Building with WSL...")
    
    # Create build script for WSL
    wsl_script = """#!/bin/bash
set -e

echo "Setting up WSL environment..."

# Update package list
sudo apt-get update

# Install dependencies
sudo apt-get install -y python3 python3-pip python3-venv python3-dev python3-tk tk-dev
sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev libwebp-dev

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build executable
python -m PyInstaller \\
    --onefile \\
    --windowed \\
    --icon=icon.png \\
    --name="Quick Image Presenter" \\
    --add-data="icon.png:." \\
    quick_image_presenter.py

# Make executable
chmod +x "dist/Quick Image Presenter"

echo "Build completed in WSL"
"""
    
    with open('build_wsl.sh', 'w') as f:
        f.write(wsl_script)
    
    try:
        # Copy files to WSL
        print("Copying files to WSL...")
        subprocess.run(['wsl', 'mkdir', '-p', '/tmp/quick-image-presenter'], check=True)
        subprocess.run(['wsl', 'cp', '-r', '.', '/tmp/quick-image-presenter/'], check=True)
        
        # Run build script in WSL
        print("Running build in WSL...")
        subprocess.run(['wsl', 'bash', '/tmp/quick-image-presenter/build_wsl.sh'], check=True)
        
        # Copy executable back to Windows
        print("Copying executable back to Windows...")
        os.makedirs('dist', exist_ok=True)
        subprocess.run(['wsl', 'cp', '/tmp/quick-image-presenter/dist/Quick Image Presenter', '/mnt/c/tmp/'], check=True)
        subprocess.run(['copy', 'C:\\tmp\\Quick Image Presenter', 'dist\\'], check=True)
        
        print("✅ Linux executable created successfully!")
        print(f"📁 Location: dist/Quick Image Presenter")
        
        # Get file size
        if os.path.exists('dist/Quick Image Presenter'):
            size = os.path.getsize('dist/Quick Image Presenter')
            print(f"📏 Size: {size / (1024*1024):.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ WSL build failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists('build_wsl.sh'):
            os.remove('build_wsl.sh')

def create_linux_build_instructions():
    """Create detailed instructions for building on Linux"""
    instructions = """# Linux Build Instructions

## Option 1: Direct Linux Build (Recommended)

If you have access to a Linux system, follow these steps:

### Prerequisites
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv python3-dev python3-tk tk-dev
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev libwebp-dev

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip python3-devel tk-devel
sudo yum install libjpeg-devel libpng-devel libtiff-devel libwebp-devel
```

### Build Steps
```bash
# Clone or copy the project to Linux
cd quick-image-presenter

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build executable
python -m PyInstaller \\
    --onefile \\
    --windowed \\
    --icon=icon.png \\
    --name="Quick Image Presenter" \\
    --add-data="icon.png:." \\
    quick_image_presenter.py

# Make executable
chmod +x "dist/Quick Image Presenter"

# Test the executable
./dist/Quick\\ Image\\ Presenter
```

## Option 2: Using the Build Script

```bash
# Make script executable
chmod +x build_linux.sh

# Run build script
./build_linux.sh
```

## Option 3: Docker Build

```bash
# Build using Docker
docker run --rm -v "$(pwd):/app" -w /app ubuntu:20.04 bash -c "
    apt-get update && apt-get install -y python3 python3-pip python3-venv python3-dev python3-tk tk-dev libjpeg-dev libpng-dev libtiff-dev libwebp-dev
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m PyInstaller --onefile --windowed --icon=icon.png --name='Quick Image Presenter' --add-data='icon.png:.' quick_image_presenter.py
    chmod +x 'dist/Quick Image Presenter'
"
```

## Distribution

The Linux executable can be distributed as:
- Single file: `dist/Quick Image Presenter`
- Size: ~20-30 MB
- Dependencies: Minimal system libraries (usually pre-installed)

## Testing

Test the executable on different Linux distributions:
- Ubuntu 18.04+
- Debian 10+
- CentOS 7+
- Fedora 30+

## Troubleshooting

1. **Permission denied**: `chmod +x "dist/Quick Image Presenter"`
2. **Missing libraries**: Install system dependencies listed above
3. **Display issues**: Ensure X11 is running or use `export DISPLAY=:0`
"""
    
    with open('Linux_Build_Instructions.txt', 'w') as f:
        f.write(instructions)
    
    print("📄 Created Linux_Build_Instructions.txt with detailed build steps")

def main():
    print("================================================")
    print("Quick Image Presenter - Linux Build Tool")
    print("================================================")
    print()
    
    current_os = platform.system()
    print(f"Current OS: {current_os}")
    
    if current_os == "Windows":
        print("\n🔍 Checking available build methods...")
        
        docker_available = check_docker()
        wsl_available = check_wsl()
        
        if docker_available:
            print("\n🐳 Docker build available")
            choice = input("Would you like to build using Docker? (y/n): ").lower()
            if choice == 'y':
                if build_with_docker():
                    return
                else:
                    print("Docker build failed, trying WSL...")
        
        if wsl_available:
            print("\n🐧 WSL build available")
            choice = input("Would you like to build using WSL? (y/n): ").lower()
            if choice == 'y':
                if build_with_wsl():
                    return
                else:
                    print("WSL build failed")
        
        print("\n❌ No suitable build method found on Windows")
        print("Creating detailed Linux build instructions...")
        create_linux_build_instructions()
        
        print("\n📋 To build the Linux executable, you have these options:")
        print("1. Use a Linux system (recommended)")
        print("2. Use WSL (Windows Subsystem for Linux)")
        print("3. Use Docker")
        print("4. Use a Linux virtual machine")
        
    elif current_os == "Linux":
        print("\n🐧 Running on Linux - using native build")
        
        # Check if required tools are available
        try:
            subprocess.run(['python3', '--version'], check=True)
            subprocess.run(['pip3', '--version'], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Python3 or pip3 not found")
            print("Please install Python 3.7+ and pip3")
            return
        
        # Run the Linux build script
        try:
            subprocess.run(['bash', 'build_linux.sh'], check=True)
            print("✅ Linux build completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Linux build failed: {e}")
            print("Please check the error messages above")
    
    else:
        print(f"❌ Unsupported OS: {current_os}")
        print("This script is designed for Windows and Linux")

if __name__ == "__main__":
    main() 