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

## Installation

1. **Prerequisites**: Python 3.7 or higher
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

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

2. **Select Image Folder**: Click "Browse" to select a folder containing your images

3. **Configure Settings**:
   - Set default display time (used when filename doesn't specify time)
   - Choose transition effect (default: Dissolve)

4. **Start Presentation**: Click "Play Presentation" to begin full-screen presentation

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

## Presentation Controls

During full-screen presentation:
- **ESC Key**: Exit presentation
- **X Button**: Exit presentation (top-right corner)
- **ℹ Button**: Show presentation info (top-right corner)
- **Timer Display**: Shows countdown for current image (top-right corner)

## License

MIT License - See the application's info dialog for full license text.

## Technical Details

- Built with Python Tkinter for cross-platform compatibility
- Uses PIL (Pillow) for image processing and resizing
- Multi-threaded timer for smooth countdown display
- Automatic image resizing to fit screen while maintaining aspect ratio
- Thread-safe presentation controls

## Troubleshooting

- **No Images Found**: Ensure the selected folder contains supported image files
- **Display Issues**: Check that images are not corrupted and are in supported formats
- **Performance**: Large images may take time to load; consider resizing images beforehand 
