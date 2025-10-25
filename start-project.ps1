#!/usr/bin/env pwsh

# AI Site Generator - PowerShell Başlatma Scripti

# Renkli çıktılar
$GREEN = "`e[32m"
$BLUE = "`e[34m"
$YELLOW = "`e[33m"
$RED = "`e[31m"
$NC = "`e[0m"

Write-Host "$BLUE AI Site Generator - Başlatılıyor... $NC"
Write-Host "=========================================="

# Python kontrolü
function Check-Python {
    Write-Host "$YELLOW Python kontrol ediliyor... $NC"
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python bulunamadı"
        }
        Write-Host "$GREEN✅ Python bulundu: $pythonVersion$NC"
    } catch {
        Write-Host "$RED❌ Python bulunamadı! Lütfen Python 3.8+ yükleyin.$NC"
        exit 1
    }
}

# Node.js kontrolü
function Check-Node {
    Write-Host "$YELLOW Node.js kontrol ediliyor... $NC"
    try {
        $nodeVersion = node --version
        Write-Host "$GREEN✅ Node.js bulundu: $nodeVersion$NC"
    } catch {
        Write-Host "$RED❌ Node.js bulunamadı! Lütfen Node.js yükleyin.$NC"
        exit 1
    }
}

# Ollama kontrolü (opsiyonel)
function Check-Ollama {
    Write-Host "$YELLOW Ollama kontrol ediliyor... $NC"
    try {
        $null = Get-Command ollama -ErrorAction Stop
        Write-Host "$GREEN✅ Ollama bulundu$NC"
    } catch {
        Write-Host "$YELLOW⚠️  Ollama bulunamadı. Mock modu kullanılacak.$NC"
        Write-Host "$YELLOW   Ollama kurmak için: https://ollama.ai/$NC"
        $env:AI_SITE_GENERATOR_MOCK = "true"
    }
}

# Backend başlatma
function Start-Backend {
    Write-Host "$YELLOW Backend başlatılıyor... $NC"
    
    # Sanal ortam oluştur/aktif et
    if (!(Test-Path ".venv")) {
    Write-Host "$YELLOW Sanal ortam oluşturuluyor... $NC"
        python -m venv .venv
    }
    
    .\.venv\Scripts\Activate.ps1
    
    # Bağımlılıkları yükle
    Write-Host "$YELLOW Python bağımlılıkları yükleniyor... $NC"
    pip install -r requirements.txt
    
    # Backend'i başlat (venv içindeki python'u kullan, uvicorn modülü ile)
    Write-Host "$GREEN Backend başlatılıyor: http://localhost:8000 $NC"
    $venvPython = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) {
        Start-Process -NoNewWindow -FilePath $venvPython -ArgumentList "-m uvicorn backend.app:app --reload"
    } else {
        # Fallback to system python
        Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn backend.app:app --reload"
    }
}

# Ana işlem
Write-Host "$BLUE🎯 AI Site Generator Kurulum Kontrolleri$NC"
Check-Python
Check-Node
Check-Ollama

Write-Host "`n$BLUE Servisler Başlatılıyor... $NC"
Start-Backend

Write-Host "`n$GREEN Backend başlatıldı! Frontend başlatmak için:$NC"
Write-Host "$BLUE cd frontend && npm install && npm run dev$NC"
Write-Host "$BLUE Frontend: ${GREEN}http://localhost:5173${NC}"
Write-Host "$BLUE Backend API: ${GREEN}http://localhost:8000${NC}"
Write-Host "$BLUE API Dokumantasyonu: ${GREEN}http://localhost:8000/docs${NC}"