#!/bin/bash
echo "Starting LegalEase Application..."

# Start FastAPI Backend in background
python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to be ready
sleep 2

# Start Streamlit Frontend
streamlit run frontend/app.py

# Cleanup on exit
kill $BACKEND_PID
