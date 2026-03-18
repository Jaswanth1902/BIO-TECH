@echo off
REM ============================================================
REM  setup.bat - One-click setup for Supply Chain Traceability
REM  Run this from the SupplyChainApp directory in cmd/PowerShell
REM ============================================================

echo [1/4] Creating Python virtual environment...
python -m venv venv
call venv\Scripts\activate

echo [2/4] Installing Python dependencies...
pip install -r requirements.txt

echo [3/4] Training the shelf-life ML model...
cd ml
python train_model.py
cd ..

echo [4/4] Building RAG knowledge-base embeddings...
cd rag
python build_kb.py
cd ..

echo.
echo ============================================================
echo  Setup complete!
echo  NEXT STEPS:
echo  1. Start Ganache (desktop app or: npx ganache)
echo  2. Run: python deploy_contract.py
echo  3. Run: python app.py
echo  4. Open  http://127.0.0.1:5000  in your browser
echo  5. Login with admin / admin123
echo ============================================================
pause
