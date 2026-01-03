FROM python:3.11-slim

WORKDIR /app

# Шаг 1: Обновление пакетов
RUN echo "=== Step 1: Updating packages ===" && \
    apt-get update && \
    echo "=== Step 1: Done ===" && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    echo "=== System packages installed ==="

# Шаг 2: Копирование requirements
COPY requirements.txt .
RUN echo "=== Step 2: Requirements copied ==="

# Шаг 3: Установка Python пакетов
RUN echo "=== Step 3: Installing Python packages ===" && \
    pip install --no-cache-dir -r requirements.txt gunicorn && \
    echo "=== Step 3: Python packages installed ==="

# Шаг 4: Копирование проекта
COPY . .
RUN echo "=== Step 4: Project files copied ==="

# Шаг 5: Collect static
RUN echo "=== Step 5: Collecting static files ===" && \
    python manage.py collectstatic --noinput || true && \
    echo "=== Step 5: Static files collected ==="

# Шаг 6: Создание пользователя
RUN echo "=== Step 6: Creating user ===" && \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    echo "=== Step 6: User created ==="

USER appuser

EXPOSE 8000

CMD python manage.py migrate && gunicorn stripe_server.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
