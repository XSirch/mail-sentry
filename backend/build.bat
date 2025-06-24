@echo off
setlocal enabledelayedexpansion

REM Script de build para o backend do Mail Categorizer (Windows)

echo 🐳 Building Mail Categorizer Backend...

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker não está instalado!
    exit /b 1
)

REM Verificar se arquivo .env existe
if not exist ".env" (
    echo [WARN] Arquivo .env não encontrado!
    echo [INFO] Copiando .env.example para .env...
    copy .env.example .env
    echo [WARN] Por favor, edite o arquivo .env com suas credenciais antes de continuar.
    pause
    exit /b 1
)

REM Build da imagem
echo [INFO] Fazendo build da imagem Docker...
docker build -t mail-categorizer-backend:latest .

if errorlevel 0 (
    echo [INFO] ✅ Build concluído com sucesso!
    
    REM Mostrar informações da imagem
    echo.
    echo [INFO] Informações da imagem:
    docker images mail-categorizer-backend:latest
    
    echo.
    echo [INFO] Para executar o container:
    echo   docker run --env-file .env mail-categorizer-backend:latest
    echo.
    echo [INFO] Para executar com docker-compose:
    echo   docker-compose up -d
    
) else (
    echo [ERROR] ❌ Falha no build!
    exit /b 1
)

pause
