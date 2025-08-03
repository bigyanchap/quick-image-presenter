@echo off
echo ================================================
echo Quick Image Presenter - Linux Build Tool
echo ================================================
echo.

echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo Python found. Running Linux build tool...
echo.

python build_linux_cross_platform.py

echo.
echo Build process completed.
pause 