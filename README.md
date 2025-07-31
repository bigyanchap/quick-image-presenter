# Quick Image Presenter

A Python desktop application for automatic image presentation with customizable display times and transition effects.

## Features

- **Folder Selection**: Choose a folder containing images to present
- **Customizable Display Time**: Set default display time for images (in seconds)
- **Transition Effects**: 10 different transition types (Dissolve, Fade, Slide, Zoom, etc.)
- **Full-Screen Presentation**: Professional full-screen presentation mode
- **Smart Timing**: Extract display time from image filenames (e.g., `image-10.jpg` = 10 seconds)
- **Automatic Progression**: Images displayed in ascending alphabetical order
- **Minimal Controls**: Only ESC key or X button to exit presentation
- **Application Icon**: Custom icon integration for professional appearance
- **Standalone Executable**: Can be built as a standalone application

## Installation

### Option 1: Run from Source
1. **Prerequisites**: Python 3.7 or higher
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Option 2: Standalone Executable
Build a standalone executable that doesn't require Python installation:

**Windows:**
```bash
build_standalone.bat
```

**Linux/macOS:**
```bash
./build_standalone.sh
```

**Manual Build:**
```bash
python build_standalone.py
```

For detailed build instructions, see [Standalone.md](Standalone.md).

## Usage

1. **Run the Application** (choose one method):
   
   **Method 1 - Direct run**:
   ```bash
   python quick_image_presenter.py
   ```
   
   **Method 2 - Using launcher** (recommended):
   ```bash
   python launcher.py
   ```
   
   **Method 3 - Windows batch file**:
   ```bash
   run_presenter.bat
   ```
   
   **Method 4 - Standalone executable** (after building):
   ```bash
   dist/Quick Image Presenter.exe  # Windows
   dist/Quick\ Image\ Presenter    # Linux/macOS
   ```

2. **Select Image Folder**: Click "Browse" to select a folder containing your images

3. **Configure Settings**:
   - Set default display time (used when filename doesn't specify time)
   - Choose transition effect (default: Dissolve)

4. **Start Presentation**: Click "🎬 Start Presentation" to begin full-screen presentation

## Image Naming Convention

The app supports extracting display time from image filenames:

- **With Time**: `1a-11.jpg` → displays for 11 seconds
- **Without Time**: `image.jpg` → uses default display time

### Examples:
- `slide1-5.jpg` → 5 seconds
- `photo-10.png` → 10 seconds  
- `image.jpg` → default time (5 seconds)

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)
- WebP (.webp)

## Transition Effects

The application includes 10 different transition effects:

1. **Dissolve**: Smooth crossfade between images
2. **Fade**: Gradual fade transition
3. **Slide Left**: Image slides in from the right
4. **Slide Right**: Image slides in from the left
5. **Slide Up**: Image slides in from the bottom
6. **Slide Down**: Image slides in from the top
7. **Zoom In**: Image zooms in from small to full size
8. **Zoom Out**: Image zooms out from large to normal size
9. **Rotate**: Simulated rotation effect
10. **Flip**: Horizontal flip transition

## Presentation Controls

During full-screen presentation:
- **ESC Key**: Exit presentation
- **X Button**: Exit presentation (top-right corner)
- **ℹ Button**: Show presentation info (top-right corner)
- **Timer Display**: Shows countdown for current image (top-left corner)
- **Image Counter**: Shows current image number and total (top-left corner)

## Building Standalone Executable

### Quick Build
Use the provided build scripts:

**Windows:**
```bash
build_standalone.bat
```

**Linux/macOS:**
```bash
./build_standalone.sh
```

### Manual Build
```bash
python build_standalone.py
```

### Advanced Build
For more control over the build process, see [Standalone.md](Standalone.md) for detailed instructions.

## Project Structure

```
quick-image-presenter/
├── quick_image_presenter.py    # Main application
├── icon.png                    # Application icon
├── requirements.txt            # Python dependencies
├── build_standalone.py         # Build script
├── build_standalone.bat        # Windows build script
├── build_standalone.sh         # Unix build script
├── Standalone.md              # Detailed build guide
├── .gitignore                 # Git ignore rules
└── dist/                      # Generated executable (after build)
```

## License

MIT License - See the application's info dialog for full license text.

## Technical Details

- Built with Python Tkinter for cross-platform compatibility
- Uses PIL (Pillow) for image processing and resizing
- Multi-threaded timer for smooth countdown display
- Automatic image resizing to fit screen while maintaining aspect ratio
- Thread-safe presentation controls
- PyInstaller for standalone executable creation
- Custom application icon integration

## Troubleshooting

### General Issues
- **No Images Found**: Ensure the selected folder contains supported image files
- **Display Issues**: Check that images are not corrupted and are in supported formats
- **Performance**: Large images may take time to load; consider resizing images beforehand

### Build Issues
- **Missing Dependencies**: Run `pip install -r requirements.txt`
- **Icon Not Loading**: Ensure `icon.png` is in the project directory
- **Large Executable**: This is normal for PyInstaller builds
- **Antivirus Warnings**: Add the executable to your antivirus whitelist

For more detailed troubleshooting, see [Standalone.md](Standalone.md). 
