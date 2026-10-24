@echo off
rem Genera dist\YTMusic.exe (un unico ejecutable, sin consola).
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" python -m venv .venv
".venv\Scripts\python.exe" -m pip install -r requirements.txt pyinstaller || exit /b 1
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --onefile --windowed --name YTMusic ^
    --collect-data imageio_ffmpeg --collect-binaries imageio_ffmpeg main.py
echo.
echo Ejecutable generado en dist\YTMusic.exe
pause
