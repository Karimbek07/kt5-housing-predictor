@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3.12 -m pip install -r requirements.txt
if errorlevel 1 echo Ошибка установки. Проверьте Python 3.12 и подключение к интернету.
pause
