@echo off
cd /d "%~dp0"
py launcher.py
if %errorlevel% neq 0 (
    echo Something went wrong!
    pause
)