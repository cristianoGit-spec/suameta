@echo off
REM Script de Deploy Automático para Railway
REM Mantém o layout responsivo e profissional

echo.
echo ========================================
echo   DEPLOY AUTOMATICO - RAILWAY
echo ========================================
echo.
echo Este script vai fazer o deploy automatico
echo da sua aplicacao no Railway.
echo.
echo Layout responsivo: MANTIDO 100%%
echo Configuracoes: AUTOMATICAS
echo.
echo ========================================
echo.

REM Verificar se Railway CLI está instalado
where railway >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Railway CLI nao encontrado!
    echo Instalando Railway CLI...
    npm install -g @railway/cli
)

echo [1/4] Fazendo login no Railway...
echo.
echo Uma janela do navegador sera aberta.
echo Faca login com sua conta GitHub.
echo.
pause

railway login

if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Login falhou. Tente novamente.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [2/4] Criando projeto no Railway...
echo ========================================
echo.

railway init

if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao criar projeto.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [3/4] Adicionando PostgreSQL...
echo ========================================
echo.

railway add --database postgres

echo.
echo ========================================
echo [4/4] Fazendo deploy da aplicacao...
echo ========================================
echo.
echo Aguarde... O Railway vai:
echo  - Instalar dependencias
echo  - Criar banco de dados
echo  - Criar tabelas automaticamente
echo  - Criar usuario admin (admin@suameta.com)
echo  - Iniciar a aplicacao
echo.

railway up

if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Deploy falhou. Verifique os logs.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   DEPLOY CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo Obtendo URL da aplicacao...
echo.

railway domain

echo.
echo ========================================
echo   ACESSO A APLICACAO
echo ========================================
echo.
echo Email: admin@suameta.com
echo Senha: admin123
echo.
echo IMPORTANTE: Altere a senha apos o primeiro login!
echo.
echo Layout responsivo: MANTIDO
echo Todas as configuracoes: AUTOMATICAS
echo.
echo ========================================
echo.
echo Para ver logs: railway logs
echo Para abrir no navegador: railway open
echo.
pause
