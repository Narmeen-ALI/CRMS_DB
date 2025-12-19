@echo off
echo ========================================
echo CRMS - Starting Python Backend Server
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

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start Flask app
python app.py

pause


