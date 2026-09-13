@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    start "Build a Hooper server" /b py -3 offline_server.py
) else (
    where python >nul 2>nul
    if not %errorlevel%==0 (
        echo Python 3 was not found. Install Python 3 and try again.
        pause
        exit /b 1
    )
    start "Build a Hooper server" /b python offline_server.py
)

timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5000/"
endlocal