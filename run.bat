@echo off
REM Quick start script for Windows

echo ========================================
echo Financial Insights Agent - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys.
    echo.
    pause
    exit /b 1
)

REM Run the application
echo Starting Financial Insights Agent...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.
streamlit run app.py

pause
