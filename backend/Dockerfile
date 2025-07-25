FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


RUN apt-get update && apt-get install -y gcc g++ libxml2-dev libxslt-dev libffi-dev libssl-dev cron && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app && \
    touch /var/log/cron.log && \
    chown app:app /var/log/cron.log

RUN echo "*/60 * * * * app python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/app-cron && \
    chmod 0644 /etc/cron.d/app-cron

CMD ["cron", "-f"]