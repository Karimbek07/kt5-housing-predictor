@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist "KT5_models_and_preprocessing.joblib" (
  echo Не найден KT5_models_and_preprocessing.joblib
  echo Скопируйте его из вашей папки KT5_Housing рядом с app.py
  pause
  exit /b 1
)
py -3.12 -m streamlit run app.py
pause
