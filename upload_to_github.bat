@echo off
setlocal
cd /d "%~dp0"
echo === KT5 Housing: GitHub publication ===
where git >nul 2>&1
if errorlevel 1 (
  echo Git is missing. Install from https://git-scm.com/downloads/win
  pause
  exit /b 1
)
git lfs version >nul 2>&1
if errorlevel 1 (
  echo Git LFS is missing. Install from https://git-lfs.com/
  pause
  exit /b 1
)
if not exist "KT5_models_and_preprocessing.joblib" (
  echo ERROR: KT5_models_and_preprocessing.joblib is missing.
  pause
  exit /b 1
)
if exist .git (
  echo This folder is already a Git repository. Stop to avoid modifying it unexpectedly.
  echo See DEPLOY.md for manual commands.
  pause
  exit /b 1
)
echo Create an EMPTY GitHub repository first: https://github.com/new
set /p REPO_URL=Paste repository HTTPS URL ending in .git: 
if "%REPO_URL%"=="" exit /b 1
set "PREFIX=%REPO_URL:~0,19%"
if /I not "%PREFIX%"=="https://github.com/" (
  echo ERROR: Expected an HTTPS GitHub URL, e.g. https://github.com/username/kt5-housing-predictor.git
  pause
  exit /b 1
)
for /f "delims=" %%A in ('git config user.name') do set "GITNAME=%%A"
for /f "delims=" %%A in ('git config user.email') do set "GITEMAIL=%%A"
if not defined GITNAME (
  echo Git user.name not configured. Run: git config --global user.name "Your Name"
  pause
  exit /b 1
)
if not defined GITEMAIL (
  echo Git user.email not configured. Run: git config --global user.email "Your GitHub email"
  pause
  exit /b 1
)
echo.
echo Destination: %REPO_URL%
echo This will create a public/restricted repository content according to GitHub visibility.
choice /C YN /M "Continue, commit, and push this project"
if errorlevel 2 exit /b 0
git init || goto failed
git lfs install || goto failed
git lfs track "KT5_models_and_preprocessing.joblib" || goto failed
git add . || goto failed
git commit -m "KT5 Housing Predictor: Streamlit and ML models" || goto failed
git branch -M main || goto failed
git remote add origin "%REPO_URL%" || goto failed
git push -u origin main || goto failed
echo.
echo SUCCESS. GitHub repository pushed.
echo Now deploy through https://share.streamlit.io/ with main / app.py
pause
exit /b 0
:failed
echo.
echo The upload did not finish. Check the error above and see DEPLOY.md.
pause
exit /b 1
