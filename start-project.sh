#!/bin/bash

# AI Site Generator - Başlatma Scripti
set -e

# Renkli çıktılar
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 AI Site Generator - Başlatılıyor...${NC}"
echo "=========================================="

# Python kontrolü
check_python() {
    echo -e "${YELLOW}🔍 Python kontrol ediliyor...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 bulunamadı! Lütfen Python 3.8+ yükleyin.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Python3 bulundu: $(python3 --version)${NC}"
}

# Node.js kontrolü
check_node() {
    echo -e "${YELLOW}🔍 Node.js kontrol ediliyor...${NC}"
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js bulunamadı! Lütfen Node.js yükleyin.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Node.js bulundu: $(node --version)${NC}"
}

# Ollama kontrolü (opsiyonel)
check_ollama() {
    echo -e "${YELLOW}🔍 Ollama kontrol ediliyor...${NC}"
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}✅ Ollama bulundu${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama bulunamadı. Mock modu kullanılacak.${NC}"
        echo -e "${YELLOW}   Ollama kurmak için: https://ollama.ai/${NC}"
        export AI_SITE_GENERATOR_MOCK=true
    fi
}

# Backend başlatma
start_backend() {
    echo -e "${YELLOW}🚀 Backend başlatılıyor...${NC}"
    
    # Sanal ortam oluştur/aktif et
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}📦 Sanal ortam oluşturuluyor...${NC}"
        python3 -m venv .venv
    fi
    
    source .venv/bin/activate
    
    # Bağımlılıkları yükle
    echo -e "${YELLOW}📦 Python bağımlılıkları yükleniyor...${NC}"
    pip install -r requirements.txt
    
    # Backend'i başlat
    echo -e "${GREEN}✅ Backend başlatılıyor: http://localhost:8000${NC}"
    python backend/app.py &
    BACKEND_PID=$!
}

# Frontend başlatma
start_frontend() {
    echo -e "${YELLOW}🚀 Frontend başlatılıyor...${NC}"
    
    cd frontend
    echo -e "${YELLOW}📦 Frontend bağımlılıkları yükleniyor...${NC}"
    npm install
    
    echo -e "${GREEN}✅ Frontend başlatılıyor...${NC}"
    npm run dev &
    FRONTEND_PID=$!
    cd ..
}

# Ana işlem
main() {
    echo -e "${BLUE}🎯 AI Site Generator Kurulum Kontrolleri${NC}"
    check_python
    check_node
    check_ollama
    
    echo -e "\n${BLUE}🚀 Servisler Başlatılıyor...${NC}"
    start_backend
    sleep 3
    start_frontend
    
    echo -e "\n${GREEN}🎉 AI Site Generator başarıyla başlatıldı!${NC}"
    echo -e "${BLUE}📍 Frontend: ${GREEN}http://localhost:5173${NC}"
    echo -e "${BLUE}📍 Backend API: ${GREEN}http://localhost:8000${NC}"
    echo -e "${BLUE}📍 API Dokümantasyon: ${GREEN}http://localhost:8000/docs${NC}"
    echo -e "\n${YELLOW}⚠️  Servisleri durdurmak için Ctrl+C tuşuna basın${NC}"
    
    # Process'leri takip et
    wait $BACKEND_PID $FRONTEND_PID
}

# Trap sinyalleri
trap 'echo -e "\n${RED}🛑 Servisler durduruluyor...${NC}"; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT TERM

# Script'i çalıştır
main
