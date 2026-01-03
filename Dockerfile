FROM python:3.11-bookworm

WORKDIR /app

# Настройка российских зеркал для Debian Bookworm
RUN echo "deb http://mirror.yandex.ru/debian/ bookworm main" > /etc/apt/sources.list && \
    echo "deb http://mirror.yandex.ru/debian/ bookworm-updates main" >> /etc/apt/sources.list && \
    echo "deb http://mirror.yandex.ru/debian-security bookworm-security main" >> /etc/apt/sources.list

# Или альтернативный вариант - использовать sources.list.d (новый формат)
# RUN echo "Types: deb\nURIs: http://mirror.yandex.ru/debian/\nSuites: bookworm bookworm-updates\nComponents: main\nSigned-By: /usr/share/keyrings/debian-archive-keyring.gpg" > /etc/apt/sources.list.d/debian.sources

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей (включая gunicorn)
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Копирование проекта
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Создание пользователя (опционально, для безопасности)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD python manage.py migrate && gunicorn stripe_server.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
