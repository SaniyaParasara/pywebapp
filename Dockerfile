# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Faster, cleaner Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps (add if needed for your libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# App listens on 8000
EXPOSE 8000

# Production entrypoint with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
