FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl libpq5 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --only-binary=:all: -r requirements.txt gunicorn

COPY . .

RUN python manage.py collectstatic --noinput || true

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD python manage.py migrate && gunicorn stripe_server.wsgi:application \
    --bind 0.0.0.0:8000 --workers 2 --timeout 120

