# Script de Inicializacao do Django
# Execute: .\iniciar_django.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  INICIANDO SISTEMA DJANGO" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# Verificar ambiente virtual
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "[ERRO] Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Ativar ambiente virtual
Write-Host "[OK] Ativando ambiente virtual..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Instalar dependencias Django
Write-Host "`n[OK] Instalando dependencias Django..." -ForegroundColor Yellow
pip install Django django-import-export django-crispy-forms crispy-bootstrap5 pillow whitenoise --quiet --disable-pip-version-check

# Guardar diretorio atual
$originalDir = Get-Location

try {
    # Definir caminho do Python
    $pythonExe = "C:/Users/JOAO/Desktop/projeto_evento/.venv/Scripts/python.exe"
    
    # Entrar na pasta webapp
    Set-Location webapp

    # Aplicar migracoes
    Write-Host "`n[OK] Configurando banco de dados..." -ForegroundColor Yellow
    & $pythonExe manage.py migrate --noinput

    # Criar migracoes do app eventos se necessario
    Write-Host "`n[OK] Verificando migracoes do app eventos..." -ForegroundColor Yellow
    & $pythonExe manage.py makemigrations eventos --noinput

    # Aplicar migracoes do eventos
    & $pythonExe manage.py migrate eventos --noinput

    # Verificar se superusuario ja existe
    Write-Host "`n[OK] Verificando superusuario..." -ForegroundColor Yellow
    $checkScript = @"
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.filter(is_superuser=True).exists())
"@
    $superuserCheck = & $pythonExe manage.py shell --command $checkScript

    if ($superuserCheck -like "*True*") {
        Write-Host "[OK] Superusuario ja existe!" -ForegroundColor Green
    } else {
        Write-Host "`n[AVISO] Nenhum superusuario encontrado!" -ForegroundColor Red
        Write-Host "[INFO] Crie um agora:" -ForegroundColor Yellow
        & $pythonExe manage.py createsuperuser
    }

    # Coletar arquivos estaticos
    Write-Host "`n[OK] Coletando arquivos estaticos..." -ForegroundColor Yellow
    & $pythonExe manage.py collectstatic --noinput --clear

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  SISTEMA PRONTO!" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Cyan

    Write-Host "[INFO] Acessos:" -ForegroundColor Yellow
    Write-Host "   Dashboard: http://localhost:8000/" -ForegroundColor White
    Write-Host "   Admin:     http://localhost:8000/admin/" -ForegroundColor White
    Write-Host "`n[INFO] Iniciando servidor..." -ForegroundColor Yellow
    Write-Host "[AVISO] Pressione Ctrl+C para parar`n" -ForegroundColor Gray

    # Iniciar servidor
    & $pythonExe manage.py runserver
}
finally {
    # Retornar ao diretorio original
    Set-Location $originalDir
}
