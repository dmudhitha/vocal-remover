@echo off
setlocal enabledelayedexpansion
title Vocal Remover App Launcher

:MENU
cls
echo ========================================
echo       Vocal Remover App Launcher
echo ========================================
echo.
echo  1. Start Web UI (Backend + Frontend)
echo  2. Run CLI Tool (Manual file input)
echo  3. Run Setup / Diagnostics
echo  4. Exit
echo.
echo ========================================
set /p choice="Select an option (1-4): "

if "%choice%"=="1" goto START_WEB
if "%choice%"=="2" goto START_CLI
if "%choice%"=="3" goto START_SETUP
if "%choice%"=="4" goto EXIT

goto MENU

:START_WEB
echo.
echo Starting Backend...
start "Vocal Remover - Backend" cmd /c "cd backend && python main.py"
echo Starting Frontend...
start "Vocal Remover - Frontend" cmd /c "cd frontend && npm.cmd run dev"
echo.
echo Web UI should be opening soon at http://localhost:5173
echo (Close the new windows to stop the servers)
echo.
pause
goto MENU

:START_CLI
echo.
set /p file_path="Enter the full path to your audio file: "
if not exist "%file_path%" (
    echo Error: File not found!
    pause
    goto MENU
)
echo Processing...
python cli/vocal_remover.py "%file_path%"
echo.
pause
goto MENU

:START_SETUP
echo.
echo Running Setup and Diagnostics...
python setup_and_run.py
echo.
pause
goto MENU

:EXIT
echo Goodbye!
exit
