#!/usr/bin/env pwsh

# AI Site Generator - PowerShell Başlatma Scripti

Write-Host "AI Site Generator - Başlatılıyor..." -ForegroundColor Cyan
Write-Host "=========================================="

# Python kontrolü
function Check-Python {
    Write-Host "Python kontrol ediliyor..." -ForegroundColor Yellow
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python bulunamadı"
        }
    Write-Host "Python bulundu: $pythonVersion" -ForegroundColor Green
    } catch {
    Write-Host "Python bulunamadı! Lütfen Python 3.8+ yükleyin." -ForegroundColor Red
        exit 1
    }
}

# Node.js kontrolü
function Check-Node {
    Write-Host "Node.js kontrol ediliyor..." -ForegroundColor Yellow
    try {
        $nodeVersion = node --version
    Write-Host "Node.js bulundu: $nodeVersion" -ForegroundColor Green
    } catch {
    Write-Host "Node.js bulunamadı! Lütfen Node.js yükleyin." -ForegroundColor Red
        exit 1
    }
}

# Ollama kontrolü (opsiyonel)
function Check-Ollama {
    Write-Host "Ollama kontrol ediliyor..." -ForegroundColor Yellow
    try {
        $null = Get-Command ollama -ErrorAction Stop
    Write-Host "Ollama bulundu" -ForegroundColor Green
    } catch {
    Write-Host "Ollama bulunamadı. Mock modu kullanılacak." -ForegroundColor Yellow
    Write-Host "Ollama kurmak için: https://ollama.ai/" -ForegroundColor Yellow
        $env:AI_SITE_GENERATOR_MOCK = "true"
    }
}

# Backend başlatma
function Start-Backend {
    Write-Host "Backend başlatılıyor..." -ForegroundColor Yellow
    
    # Sanal ortam oluştur/aktif et
    if (!(Test-Path ".venv")) {
        Write-Host "Sanal ortam oluşturuluyor..." -ForegroundColor Yellow
        python -m venv .venv
    }
    
    .\.venv\Scripts\Activate.ps1
    
    # Bağımlılıkları yükle
    Write-Host "Python bağımlılıkları yükleniyor..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    # Backend'i başlat (venv içindeki python'u kullan, uvicorn modülü ile)
    Write-Host "Backend başlatılıyor: http://localhost:8000" -ForegroundColor Green
    $venvPython = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) {
        $cmd = "& `"$venvPython`" -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000"
    } else {
        # Fallback to system python
        $cmd = "& python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000"
    }
    # Start backend in a new PowerShell window so logs are visible
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", $cmd
}

# Ana işlem
Write-Host "$BLUE🎯 AI Site Generator Kurulum Kontrolleri$NC"
Check-Python
Check-Node
Check-Ollama

Write-Host "`nServisler Başlatılıyor..." -ForegroundColor Cyan
Start-Backend

Write-Host "`nBackend başlatıldı (yeni pencerede). Frontend'i başlatıyorum..." -ForegroundColor Green

# Start frontend in a new window so Vite logs are visible
$frontendCmd = "cd `"$(Join-Path (Get-Location) 'frontend')`"; npm install; npm run dev"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host "Frontend should open in a new window. If not, run 'cd frontend; npm run dev' manually." -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Blue
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Blue
Write-Host "API Dokumantasyonu: http://localhost:8000/docs" -ForegroundColor Blue