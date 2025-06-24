FROM python:3.12-slim-bookworm


# Instalar dependências do sistema, incluindo ferramentas para compilar extensões Rust
RUN apt-get update && apt-get install -y build-essential curl gcc g++ libffi-dev && rm -rf /var/lib/apt/lists/*

# Instalar Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# Criar usuário não-privilegiado
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copiar apenas requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte e arquivos estáticos
COPY . .

# Garantir que os diretórios existam e tenham permissões corretas
RUN mkdir -p /app/static && \
    mkdir -p /app/templates && \
    chmod -R 755 /app/static /app/templates

# Mudar para o usuário não-privilegiado para execução
# (mas não durante a construção, pois precisamos de permissões de root)
USER appuser

# Expor a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
