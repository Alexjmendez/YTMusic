@echo off
rem Crea el entorno virtual la primera vez, instala dependencias y lanza la app.
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
    echo Creando entorno virtual...
    python -m venv .venv || goto :nopython
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto :error
)
rem yt-dlp se actualiza a menudo para seguir funcionando con YouTube
".venv\Scripts\python.exe" -m pip install --quiet --upgrade yt-dlp
start "" ".venv\Scripts\pythonw.exe" main.py
exit /b 0

:nopython
echo No se encontro Python. Instalalo desde https://www.python.org/downloads/ (marca "Add python.exe to PATH").
pause
exit /b 1

:error
echo Error instalando dependencias.
pause
exit /b 1
