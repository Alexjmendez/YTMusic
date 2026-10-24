@echo off
rem Genera dist\YTMusic-Setup-x.y.z.exe: instalador para otros PC (no necesitan Python ni git).
rem Requiere Inno Setup 6:  winget install JRSoftware.InnoSetup
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" python -m venv .venv
".venv\Scripts\python.exe" -m pip install --upgrade -r requirements.txt pyinstaller || exit /b 1
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --onedir --windowed --name YTMusic ^
    --collect-data imageio_ffmpeg --collect-binaries imageio_ffmpeg main.py || exit /b 1

set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
    echo No se encontro Inno Setup 6. Instalalo con: winget install JRSoftware.InnoSetup
    pause
    exit /b 1
)
"%ISCC%" installer.iss || exit /b 1
echo.
echo Instalador generado en la carpeta dist\
pause
