FROM python:3.12.11-alpine3.22

# Criar usuário não-privilegiado
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copiar apenas requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Mudar para o usuário não-privilegiado
USER appuser

# Expor a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
