@echo off
REM ============================================================
REM  run_app.bat - Easy launcher for Flask App
REM  This activates the correct local venv automatically.
REM ============================================================
echo [Bio-Tech Supply Chain] Activating local virtual environment...
cd /d "%~dp0"
call venv\Scripts\activate
echo [Bio-Tech Supply Chain] Starting Flask application...
python app.py
pause
