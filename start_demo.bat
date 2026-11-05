@echo off
cd /d "%~dp0"
echo Starting the Customer Churn demo...
echo The app will open in your browser at http://localhost:8501
python -m streamlit run app.py
pause
