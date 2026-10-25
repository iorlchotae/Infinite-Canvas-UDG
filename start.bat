@echo off
cd /d "%~dp0"

set "PYEXE=%~dp0python\python.exe"
if not exist "%PYEXE%" set "PYEXE=python"

REM ---- Dependency self-check: auto-install if missing (offline packages first) ----
"%PYEXE%" -c "import requests, fastapi, uvicorn, PIL, multipart, httpx" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Missing dependencies. Installing...
    echo.
    call "%~dp0install-deps.bat" nopause
    if errorlevel 1 (
        echo.
        echo [ERROR] Dependency installation failed.
        echo Please run install-deps.bat manually and check the messages above.
        pause
        exit /b 1
    )
    REM Re-check after install
    "%PYEXE%" -c "import requests, fastapi, uvicorn, PIL, multipart, httpx" >nul 2>&1
    if errorlevel 1 (
        echo.
        echo [ERROR] Dependencies still missing after install.
        echo Please run install-deps.bat manually and check the messages above.
        pause
        exit /b 1
    )
    echo [OK] Dependencies ready.
    echo.
)

REM ---- Port probe: fall back to next free port if 3000 is taken ----
set "PORTFILE=%TEMP%\infinite_canvas_udg.port"
set "PORT=3000"
"%PYEXE%" "%~dp0tools\pick_port.py" 3000 20 > "%PORTFILE%" 2>nul
if exist "%PORTFILE%" set /p PORT=<"%PORTFILE%"
del "%PORTFILE%" >nul 2>&1
set "CANVAS_PORT=%PORT%"

echo Starting Infinite Canvas UDG ...
echo Visit: http://127.0.0.1:%PORT%/
echo Press Ctrl+C to stop.
echo.

REM Browser is opened automatically by main.py once the server is ready.
"%PYEXE%" main.py

echo.
echo Server stopped.
pause
