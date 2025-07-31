# Creating Standalone Executable for Quick Image Presenter

This guide will walk you through creating a standalone executable for the Quick Image Presenter application using PyInstaller.

If you want it without creating it yourself, the standalone file is in /dist folder.

## Prerequisites

1. **Python 3.7+** installed on your system
2. **pip** (Python package installer)
3. **Git** (optional, for version control)

## Step 1: Install Dependencies

First, install the required packages:

```bash
pip install -r requirements.txt
```

Or install them individually:

```bash
pip install Pillow>=9.0.0
pip install pyinstaller>=5.0.0
```

## Step 2: Prepare Your Files

Ensure you have the following files in your project directory:

- `quick_image_presenter.py` - Main application file
- `icon.png` - Application icon (optional but recommended)
- `requirements.txt` - Dependencies list

## Step 3: Create the Executable

### Option A: Basic PyInstaller Command

**Windows:**
```bash
python -m PyInstaller --onefile --windowed --icon=icon.png quick_image_presenter.py
```

**Linux/macOS:**
```bash
pyinstaller --onefile --windowed --icon=icon.png quick_image_presenter.py
```

### Option B: Advanced PyInstaller Command (Recommended)

**Windows:**
```bash
python -m PyInstaller --onefile --windowed --icon=icon.png --name="Quick Image Presenter" --add-data="icon.png;." quick_image_presenter.py
```

**Linux/macOS:**
```bash
pyinstaller --onefile --windowed --icon=icon.png --name="Quick Image Presenter" --add-data="icon.png;." quick_image_presenter.py
```

### Option C: Using a Spec File (Most Control)

1. Generate a spec file:
```bash
pyi-makespec --onefile --windowed --icon=icon.png quick_image_presenter.py
```

2. Edit the generated `quick_image_presenter.spec` file to include additional data:
```python
# Add this to the Analysis section
datas=[('icon.png', '.')],
```

3. Build using the spec file:
```bash
pyinstaller quick_image_presenter.spec
```

## Step 4: Locate Your Executable

After successful compilation, your executable will be located in:
- **Windows**: `dist/Quick Image Presenter.exe`
- **macOS**: `dist/Quick Image Presenter`
- **Linux**: `dist/Quick Image Presenter`

## PyInstaller Options Explained

- `--onefile`: Creates a single executable file
- `--windowed`: Prevents console window from appearing (Windows/macOS)
- `--icon=icon.png`: Sets the application icon
- `--name="Quick Image Presenter"`: Sets the executable name
- `--add-data="icon.png;."`: Includes the icon file in the executable

## Troubleshooting

### Common Issues and Solutions

1. **Missing Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **PyInstaller Not Found (Windows)**
   ```bash
   # Use Python module approach instead of direct command
   python -m PyInstaller --onefile --windowed --icon=icon.png quick_image_presenter.py
   ```

3. **Virtual Environment Issues**
   ```bash
   # If using a virtual environment, activate it first
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/macOS
   
   # Then install PyInstaller in the virtual environment
   python -m pip install pyinstaller
   
   # Now build the executable
   python -m PyInstaller --onefile --windowed --icon=icon.png quick_image_presenter.py
   ```

2. **Icon Not Loading**
   - Ensure `icon.png` is in the same directory as your Python file
   - Use `--add-data="icon.png;."` to include the icon in the executable

3. **Large Executable Size**
   - This is normal for PyInstaller executables
   - The executable includes Python runtime and all dependencies

4. **Antivirus False Positives**
   - Some antivirus software may flag PyInstaller executables
   - Add the executable to your antivirus whitelist

5. **Permission Errors (Linux/macOS)**
   ```bash
   chmod +x dist/Quick\ Image\ Presenter
   ```

### Platform-Specific Notes

**Windows:**
- Use `--windowed` to hide the console
- Executable will be `.exe` file
- May need to run as administrator for some operations

**macOS:**
- Use `--windowed` to create a proper macOS app
- May need to sign the app for distribution
- Consider using `--codesign-identity` for code signing

**Linux:**
- Use `--onefile` for single executable
- May need to install additional libraries: `sudo apt-get install python3-dev`

## Distribution

### Windows
- The `.exe` file can be distributed directly
- Users can run it without installing Python
- Consider creating an installer using tools like Inno Setup

### macOS
- The executable can be distributed directly
- Consider creating a `.dmg` file for easier distribution
- May need to notarize the app for macOS Catalina+

### Linux
- The executable can be distributed directly
- Consider creating a `.deb` or `.rpm` package
- May need to include additional system dependencies

## Advanced Configuration

### Custom Spec File Example

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['quick_image_presenter.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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

## Performance Tips

1. **Use `--onefile`** for single executable distribution
2. **Use `--windowed`** to hide console on Windows/macOS
3. **Exclude unnecessary modules** using `--exclude-module`
4. **Use UPX compression** (included with PyInstaller) to reduce size
5. **Test thoroughly** on target platforms before distribution

## Version Control

Add the following to your `.gitignore`:
```
dist/
build/
*.spec
__pycache__/
*.pyc
```

This ensures build artifacts don't clutter your repository.

## Support

If you encounter issues:
1. Check PyInstaller documentation: https://pyinstaller.readthedocs.io/
2. Ensure all dependencies are properly installed
3. Test on a clean system to verify standalone functionality
4. Check platform-specific requirements for your target OS 