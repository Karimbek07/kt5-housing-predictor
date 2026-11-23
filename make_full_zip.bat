@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -3.12 make_full_zip.py
pause
