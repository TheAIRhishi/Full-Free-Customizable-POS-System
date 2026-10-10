@echo off
setlocal
title Dev Tribhoomi POS - setup
cd /d "%~dp0"
echo.
echo  Dev Tribhoomi POS - one-time setup
echo  ==================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo  Python is not installed.
    echo  1. Download Python 3.12 from https://www.python.org/downloads/windows/
    echo  2. During install, tick "Add python.exe to PATH".
    echo  3. Run this setup again.
    pause
    exit /b 1
  )
  set PY=python
)
%PY% -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
  echo  Python 3.10 or newer is needed. Please install Python 3.12 and run this again.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo  Creating the program environment...
  %PY% -m venv .venv || (echo  Could not create the environment. & pause & exit /b 1)
)
echo  Installing components (needs internet, a few minutes the first time)...
".venv\Scripts\python.exe" -m pip install --upgrade pip >nul
".venv\Scripts\python.exe" -m pip install -r requirements.txt || (echo  Install failed. Check the internet connection and try again. & pause & exit /b 1)
echo  Creating desktop shortcuts...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$s=New-Object -ComObject WScript.Shell; $d=[Environment]::GetFolderPath('Desktop');" ^
  "$l=$s.CreateShortcut(\"$d\Dev Tribhoomi POS.lnk\"); $l.TargetPath='%~dp0.venv\Scripts\pythonw.exe'; $l.Arguments='\"%~dp0launcher.py\"'; $l.WorkingDirectory='%~dp0'; $l.Save();" ^
  "$p=$s.CreateShortcut(\"$d\Dev Tribhoomi POS - Practice.lnk\"); $p.TargetPath='%~dp0.venv\Scripts\pythonw.exe'; $p.Arguments='\"%~dp0launcher.py\" --practice'; $p.WorkingDirectory='%~dp0'; $p.Save()"
echo.
echo  Done. Two shortcuts are on the desktop:
echo    Dev Tribhoomi POS            - the real shop
echo    Dev Tribhoomi POS - Practice - sample data for training (login owner / practice)
echo.
pause
