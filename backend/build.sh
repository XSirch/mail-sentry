#!/bin/bash

# Script de build para o backend do Mail Categorizer

set -e

echo "🐳 Building Mail Categorizer Backend..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    log_error "Docker não está instalado!"
    exit 1
fi

# Verificar se arquivo .env existe
if [ ! -f ".env" ]; then
    log_warn "Arquivo .env não encontrado!"
    log_info "Copiando .env.example para .env..."
    cp .env.example .env
    log_warn "Por favor, edite o arquivo .env com suas credenciais antes de continuar."
    exit 1
fi

# Build da imagem
log_info "Fazendo build da imagem Docker..."
docker build -t mail-categorizer-backend:latest .

if [ $? -eq 0 ]; then
    log_info "✅ Build concluído com sucesso!"
    
    # Mostrar informações da imagem
    echo ""
    log_info "Informações da imagem:"
    docker images mail-categorizer-backend:latest
    
    echo ""
    log_info "Para executar o container:"
    echo "  docker run --env-file .env mail-categorizer-backend:latest"
    echo ""
    log_info "Para executar com docker-compose:"
    echo "  docker-compose up -d"
    
else
    log_error "❌ Falha no build!"
    exit 1
fi
