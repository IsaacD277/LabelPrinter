@echo off
echo Starting Flask Label Printing Service...
cd /d "C:\Users\LabelPrinter\Documents\Python\Label Printer"

REM Load environment variables
call ../LabelPrinter/.env.bat

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo Starting server on http://%SERVER_HOST%:%SERVER_PORT%
echo Press Ctrl+C to stop the server
waitress-serve --host %SERVER_HOST% --port %SERVER_PORT% --threads 4 app:app

pause