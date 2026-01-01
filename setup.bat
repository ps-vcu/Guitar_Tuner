@echo off
echo ========================================
echo    Guitar Tuner - First Time Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b
)

echo Python detected!
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages
    echo Trying to install individually...
    pip install streamlit
    pip install numpy
    pip install scipy
    pip install sounddevice
)

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo To run the Guitar Tuner, double-click: run_tuner.bat
echo.
pause
