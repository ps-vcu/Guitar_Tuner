@echo off
echo ========================================
echo    Guitar Tuner App Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Starting Guitar Tuner...
echo.
echo The app will open in your browser.
echo Press Ctrl+C in this window to stop the app.
echo.

REM Run the Streamlit app
streamlit run guitar_tuner.py

pause
