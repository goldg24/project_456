@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  set "PROJECT_PYTHON=python"
) else (
  set "PROJECT_PYTHON=py"
)
%PROJECT_PYTHON% -m pip install -r requirements.txt
if errorlevel 1 (
  echo Dependencies could not be installed. Check the error above.
  pause
  exit /b 1
)
%PROJECT_PYTHON% -m streamlit run app.py
if errorlevel 1 pause
