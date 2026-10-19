@echo off
REM ============================================================
REM  GestureMouse - One-Click Setup and Run Script (Windows)
REM ============================================================
REM  What this does:
REM    1. Checks that Python is installed.
REM    2. Creates a local virtual environment folder called "venv"
REM       (only the first time you run this).
REM    3. Installs all required packages into that venv.
REM    4. Launches main.py using that venv's Python.
REM
REM  You can just double-click this file every time you want to
REM  run the app. No manual typing needed.
REM ============================================================

setlocal

echo ============================================
echo   GestureMouse - Setup and Launch
echo ============================================

REM ---- Step 1: Check Python is installed ----
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found on this system.
    echo Please install Python 3.9 - 3.11 from https://www.python.org/downloads/
    echo IMPORTANT: During install, check the box "Add Python to PATH".
    pause
    exit /b 1
)

REM ---- Step 2: Create virtual environment if it doesn't exist yet ----
if not exist "venv\" (
    echo [INFO] Creating virtual environment "venv" ...
    python -m venv venv
) else (
    echo [INFO] Virtual environment already exists. Skipping creation.
)

REM ---- Step 3: Activate venv and install dependencies ----
echo [INFO] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat

python -m pip install --upgrade pip >nul
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Something went wrong while installing dependencies.
    pause
    exit /b 1
)

REM ---- Step 4: Run the application ----
echo [INFO] Launching GestureMouse...
echo Press 'q' or ESC inside the camera window to quit the app.
python main.py

echo [INFO] GestureMouse has closed.
pause
