@echo off
echo ==================================================
echo INSTALANDO DEPENDENCIAS E INICIANDO O PORTAL...
echo ==================================================
pip install -r requirements.txt
echo.
echo INICIANDO O SERVIDOR...
python -m streamlit run app.py
pause
