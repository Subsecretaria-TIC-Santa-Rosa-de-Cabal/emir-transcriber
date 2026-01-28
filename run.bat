@echo off
cd /d %~dp0

echo ===============================
echo Verificando entorno virtual...
echo ===============================

if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate

echo ===============================
echo Verificando FFmpeg...
echo ===============================

where ffmpeg >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo FFmpeg no encontrado.
    echo Intentando instalar FFmpeg con winget...
    winget install --id=Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements
) else (
    echo FFmpeg ya esta instalado.
)

echo ===============================
echo Instalando dependencias Python...
echo ===============================

pip install -r requirements.txt

echo ===============================
echo Actualizando Python...
echo ===============================

python.exe -m pip install --upgrade pip

echo ===============================
echo Iniciando FastAPI...
echo ===============================

start cmd /k fastapi run src/main.py

timeout /t 2 >nul

echo Abriendo navegador...
start http://127.0.0.1:8000/
