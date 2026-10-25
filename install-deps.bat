@echo off
cd /d "%~dp0"

REM Usage: install-deps.bat [nopause]
REM   nopause = skip the final pause when called automatically from start.bat

set "NOPAUSE=%~1"

if not "%NOPAUSE%"=="nopause" (
    echo ============================================
    echo   Install Dependencies - Infinite Canvas UDG
    echo ============================================
    echo.
)

set "PYEXE=%~dp0python\python.exe"

if exist "%PYEXE%" (
    echo [OK] Using bundled Python
) else (
    echo [INFO] Bundled Python not found, trying system Python...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python not found.
        echo Please put the extracted python folder in the same directory.
        if not "%NOPAUSE%"=="nopause" pause
        exit /b 1
    )
    set "PYEXE=python"
    echo [OK] Using system Python
)

echo.

"%PYEXE%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [1/3] Installing pip via get-pip.py...
    if not exist "%~dp0get-pip.py" (
        echo Downloading get-pip.py...
        powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%~dp0get-pip.py'" 2>nul
        if not exist "%~dp0get-pip.py" (
            echo [ERROR] Failed to download get-pip.py. Check network connection.
            if not "%NOPAUSE%"=="nopause" pause
            exit /b 1
        )
    )
    "%PYEXE%" "%~dp0get-pip.py" --quiet
    if errorlevel 1 (
        echo [ERROR] Failed to install pip.
        if not "%NOPAUSE%"=="nopause" pause
        exit /b 1
    )
    echo [OK] pip installed.
)

echo.
echo [2/3] Trying offline install from packages folder...
"%PYEXE%" -m pip install --no-index --find-links=packages -r requirements.txt
if not errorlevel 1 (
    echo.
    echo [OK] Offline install succeeded.
    goto :extra
)

echo [INFO] Offline install not available for this Python, trying online install...
"%PYEXE%" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Install failed. Check your network connection.
    if not "%NOPAUSE%"=="nopause" pause
    exit /b 1
)

:extra
echo.
echo [Extra] Installing WebSocket support for Uvicorn...
"%PYEXE%" -m pip install --no-index --find-links=packages websockets
if errorlevel 1 (
    echo [WARN] Failed to install websockets. WebSocket features may be unavailable.
)

if not "%NOPAUSE%"=="nopause" (
    echo.
    echo ============================================
    echo   Done. Run start.bat to launch the server.
    echo ============================================
    pause
)

exit /b 0
