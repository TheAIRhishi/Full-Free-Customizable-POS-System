@echo off
setlocal
title %~n0
cd /d "%~dp0"

rem Read config.json and extract name values using PowerShell
for /f "usebackq delims=" %%i in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$cfg = Get-Content -Raw -Path '.\config.json' | ConvertFrom-Json; Write-Output $cfg.company.display_name"`) do set COMPANY_DISPLAY_NAME=%%i
for /f "usebackq delims=" %%i in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$cfg = Get-Content -Raw -Path '.\config.json' | ConvertFrom-Json; Write-Output $cfg.company.internal_id"`) do set COMPANY_ID=%%i

echo.
echo  %COMPANY_DISPLAY_NAME% - one-time setup
echo  ==================================
echo.

rem ... existing install flow unchanged ...
rem After the shortcuts are created:
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$s=New-Object -ComObject WScript.Shell; $d=[Environment]::GetFolderPath('Desktop');" ^
  "$l=$s.CreateShortcut(\"$d\%COMPANY_DISPLAY_NAME%.lnk\"); $l.TargetPath='%~dp0.venv\Scripts\pythonw.exe'; $l.Arguments='\"%~dp0launcher.py\"'; $l.WorkingDirectory='%~dp0'; $l.Save();" ^
  "$p=$s.CreateShortcut(\"$d\%COMPANY_DISPLAY_NAME% - Practice.lnk\"); $p.TargetPath='%~dp0.venv\Scripts\pythonw.exe'; $p.Arguments='\"%~dp0launcher.py\" --practice'; $p.WorkingDirectory='%~dp0'; $p.Save();"

echo.
echo  Done. Two shortcuts are on the desktop:
echo    %COMPANY_DISPLAY_NAME%            - the real shop
echo    %COMPANY_DISPLAY_NAME% - Practice - sample data for training
echo.
pause
