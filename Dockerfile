FROM python:3.11-bookworm

RUN sed -i 's|http://deb.debian.org|http://mirror.yandex.ru|g' /etc/apt/sources.list && \
    sed -i 's|http://security.debian.org|http://mirror.yandex.ru/debian-security|g' /etc/apt/sources.list

WORKDIR /app

RUN apt-get update && apt-get install -y curl libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD python manage.py migrate && gunicorn stripe_server.wsgi:application --bind 0.0.0.0:8000

