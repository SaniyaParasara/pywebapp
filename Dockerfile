# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Faster, cleaner Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install deps (add system libs only if your packages need them)
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# The app should bind to 0.0.0.0:8000
EXPOSE 8000

# Start the app (adjust if your entry file isn't app.py)
CMD ["python", "app.py"]
# For production (if you add gunicorn to requirements.txt), prefer:
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
