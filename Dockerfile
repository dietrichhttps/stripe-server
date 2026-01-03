FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements
COPY requirements.txt .

# Устанавливаем Python зависимости (БЕЗ --only-binary)
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Копируем проект
COPY . .

# Collect static (до смены пользователя)
RUN python manage.py collectstatic --noinput || true

# Создаем пользователя
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD python manage.py migrate && gunicorn stripe_server.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
