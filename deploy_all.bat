@echo off
REM ============================================================
REM  deploy_all.bat - One-click compiler, deployer, and launcher
REM ============================================================
cd /d "%~dp0"
echo [1/3] Activating local virtual environment...
call venv\Scripts\activate

echo [2/3] Compiling and deploying SupplyChainTrace.sol to Ganache...
python deploy_contract.py

echo [3/3] Starting Flask application...
python app.py
pause
