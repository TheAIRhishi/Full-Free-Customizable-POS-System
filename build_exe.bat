@echo off
rem Builds a standalone program folder (no Python needed on the till): dist\DevTribhoomiPOS\DevTribhoomiPOS.exe
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" call install_windows.bat
".venv\Scripts\python.exe" -m pip install pyinstaller || (pause & exit /b 1)
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --windowed --name DevTribhoomiPOS ^
  --add-data "devpos\core\schema.sql;devpos\core" ^
  --add-data "devpos\docs;devpos\docs" ^
  --collect-all nepali_datetime ^
  --hidden-import win32print ^
  launcher.py || (echo Build failed. & pause & exit /b 1)
echo.
echo Built: dist\DevTribhoomiPOS\DevTribhoomiPOS.exe
echo Copy the whole dist\DevTribhoomiPOS folder to the till computer.
pause
