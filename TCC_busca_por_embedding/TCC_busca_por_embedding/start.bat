@echo off
echo ========================================
echo   Sistema de Busca Semantica - TCC
echo ========================================
echo.

echo Verificando se o Python esta instalado...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale o Python 3.8+ e tente novamente.
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Navegando para a pasta backend...
cd backend

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando servidor...
echo.
echo ========================================
echo   Servidor rodando em: http://localhost:5000
echo   Frontend: abra frontend/index.html
echo   Para parar: Ctrl+C
echo ========================================
echo.

python run.py

pause
