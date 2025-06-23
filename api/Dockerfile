FROM python:3.12.11-alpine3.22


# Instalar dependências do sistema, incluindo ferramentas para compilar extensões Rust
RUN apk update && apk add --no-cache build-base curl gcc g++ libffi-dev

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

# Copiar o código da aplicação
COPY . .

# Mudar para o usuário não-privilegiado para execução
# (mas não durante a construção, pois precisamos de permissões de root)
USER appuser

# Expor a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
