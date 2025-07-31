@echo off
echo ================================================
echo Quick Image Presenter - Standalone Build
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Building standalone executable...
echo.

REM Run the build script
python build_standalone.py

if errorlevel 1 (
    echo.
    echo Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo Your executable is in the 'dist' folder.
echo.
pause 