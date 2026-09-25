@echo off
echo Starting LegalEase AI Legal Document Generator...
echo.

:: Start FastAPI Backend in background
start "LegalEase FastAPI Backend" cmd /k "python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload"

:: Give backend a moment to initialize
timeout /t 2 /nobreak >nul

:: Start Streamlit Frontend
start "LegalEase Streamlit Frontend" cmd /k "streamlit run frontend/app.py"

echo LegalEase is launching!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8501
