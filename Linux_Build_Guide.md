# Linux Standalone Build Guide

This guide will help you create a Linux standalone executable for the Quick Image Presenter application.

## Prerequisites

### System Requirements
- **Linux Distribution**: Ubuntu 18.04+, Debian 10+, CentOS 7+, or similar
- **Python**: 3.7 or higher
- **System Libraries**: Tkinter and image processing libraries

### Install System Dependencies

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

## Quick Build (Recommended)

### Option 1: Using the Build Script
```bash
# Make the script executable
chmod +x build_linux.sh

# Run the build script
./build_linux.sh
```

### Option 2: Manual Build
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
```

## Running the Application

### Make Executable
```bash
chmod +x "dist/Quick Image Presenter"
```

### Run the Application
```bash
./dist/Quick\ Image\ Presenter
```

## Distribution

### Single Executable
The standalone executable can be distributed as a single file:
- **File**: `dist/Quick Image Presenter`
- **Size**: Approximately 20-30 MB
- **Dependencies**: Minimal system libraries (usually pre-installed)

### Creating a Package

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

## Troubleshooting

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

## Testing

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

## Advanced Configuration

### Custom Spec File
Create `quick_image_presenter_linux.spec`:
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['quick_image_presenter.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')],
    hiddenimports=['tkinter', 'PIL', 'PIL.Image', 'PIL.ImageTk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Quick Image Presenter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.png'
)
```

Then build using:
```bash
python -m PyInstaller quick_image_presenter_linux.spec
```

## Support

For issues specific to Linux builds:
1. Check system dependencies are installed
2. Verify Python version (3.7+)
3. Ensure virtual environment is activated
4. Check file permissions
5. Verify display settings for GUI applications

## Cross-Platform Considerations

- **Windows**: Uses `.exe` files
- **macOS**: Uses `.app` bundles
- **Linux**: Uses ELF binaries

Each platform requires its own build process and executable format. 