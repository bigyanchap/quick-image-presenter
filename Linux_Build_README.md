# Quick Image Presenter - Linux Build Guide

This guide provides multiple methods to create a Linux executable for the Quick Image Presenter application.

## 🚀 Quick Start

### Option 1: Automated Build (Windows)
```bash
# Run the automated build tool
python build_linux_cross_platform.py
```

### Option 2: Direct Linux Build
```bash
# Make the script executable
chmod +x build_linux.sh

# Run the build script
./build_linux.sh
```

## 📋 Prerequisites

### System Requirements
- **Linux Distribution**: Ubuntu 18.04+, Debian 10+, CentOS 7+, or similar
- **Python**: 3.7 or higher
- **System Libraries**: Tkinter and image processing libraries

### Required System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
sudo apt-get install python3-dev python3-tk tk-dev
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev libwebp-dev
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install python3 python3-pip python3-devel
sudo yum install tk-devel
sudo yum install libjpeg-devel libpng-devel libtiff-devel libwebp-devel
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip tk
sudo pacman -S libjpeg-turbo libpng libtiff libwebp
```

## 🔧 Build Methods

### Method 1: Native Linux Build (Recommended)

If you have access to a Linux system:

```bash
# Clone or download the project
cd quick-image-presenter

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build the executable
python -m PyInstaller \
    --onefile \
    --windowed \
    --icon=icon.png \
    --name="Quick Image Presenter" \
    --add-data="icon.png:." \
    quick_image_presenter.py

# Make executable
chmod +x "dist/Quick Image Presenter"

# Test the executable
./dist/Quick\ Image\ Presenter
```

### Method 2: Using the Build Script

```bash
# Make script executable
chmod +x build_linux.sh

# Run build script
./build_linux.sh
```

### Method 3: Docker Build (Cross-platform)

If you have Docker installed:

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

### Method 4: WSL Build (Windows)

If you have WSL installed on Windows:

```bash
# Install WSL if not already installed
wsl --install

# Open WSL and navigate to project
wsl
cd /mnt/c/path/to/quick-image-presenter

# Follow the native Linux build steps above
```

## 📦 Distribution

### Single Executable
The Linux executable can be distributed as a single file:
- **File**: `dist/Quick Image Presenter`
- **Size**: Approximately 20-30 MB
- **Dependencies**: Minimal system libraries (usually pre-installed)

### Creating Packages

**For Ubuntu/Debian (.deb):**
```bash
# Install packaging tools
sudo apt-get install checkinstall

# Create package
sudo checkinstall --pkgname="quick-image-presenter" \
                  --pkgversion="2.0" \
                  --backup=no \
                  --fstrans=no \
                  --default
```

**For RPM-based systems (.rpm):**
```bash
# Install packaging tools
sudo yum install rpm-build

# Create package (requires spec file)
rpmbuild -bb quick-image-presenter.spec
```

## 🧪 Testing

### Test on Different Distributions
```bash
# Test on Ubuntu
docker run -it ubuntu:20.04 bash
# Follow installation steps above

# Test on CentOS
docker run -it centos:7 bash
# Follow installation steps above
```

### Test Dependencies
```bash
# Check if all required libraries are included
ldd "dist/Quick Image Presenter"

# Check for missing dependencies
./dist/Quick\ Image\ Presenter --help
```

## 🔧 Troubleshooting

### Common Issues

1. **"No module named 'tkinter'"**
   ```bash
   # Install tkinter
   sudo apt-get install python3-tk  # Ubuntu/Debian
   sudo yum install tkinter         # CentOS/RHEL
   ```

2. **"No module named 'PIL'"**
   ```bash
   # Install Pillow
   pip install Pillow
   ```

3. **"Permission denied"**
   ```bash
   # Make executable
   chmod +x "dist/Quick Image Presenter"
   ```

4. **"Library not found" errors**
   ```bash
   # Install missing libraries
   sudo apt-get install libjpeg-dev libpng-dev libtiff-dev
   ```

5. **Display issues (X11)**
   ```bash
   # For headless systems or SSH
   export DISPLAY=:0
   # Or use Xvfb for virtual display
   sudo apt-get install xvfb
   xvfb-run ./dist/Quick\ Image\ Presenter
   ```

### Performance Optimization

1. **Reduce executable size:**
   ```bash
   # Exclude unnecessary modules
   python -m PyInstaller \
       --onefile \
       --windowed \
       --exclude-module matplotlib \
       --exclude-module numpy \
       --exclude-module scipy \
       quick_image_presenter.py
   ```

2. **Use UPX compression:**
   ```bash
   # Install UPX
   sudo apt-get install upx

   # Compress executable
   upx --best "dist/Quick Image Presenter"
   ```

## 📁 File Structure

After a successful build, you'll have:

```
quick-image-presenter/
├── dist/
│   └── Quick Image Presenter    # Linux executable
├── build/                       # Build artifacts
├── __pycache__/                # Python cache
└── *.spec                      # PyInstaller spec files
```

## 🎯 Features of the Linux Executable

- **Standalone**: No Python installation required on target system
- **Cross-distribution**: Works on most Linux distributions
- **GUI Support**: Full Tkinter GUI functionality
- **Image Processing**: Supports multiple image formats
- **System Integration**: Proper sleep prevention and display management

## 📞 Support

For issues specific to Linux builds:
1. Check system dependencies are installed
2. Verify Python version (3.7+)
3. Ensure virtual environment is activated
4. Check file permissions
5. Verify display settings for GUI applications

## 🔄 Cross-Platform Considerations

- **Windows**: Uses `.exe` files
- **macOS**: Uses `.app` bundles
- **Linux**: Uses ELF binaries

Each platform requires its own build process and executable format.

## 📝 License

This project is licensed under the MIT License. See the main README for details. 