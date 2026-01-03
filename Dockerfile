FROM python:3.11-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    curl \
    postgresql-dev \
    || true

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create non-root user
RUN adduser -D -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run migrations and start server with gunicorn
CMD python manage.py migrate && gunicorn stripe_server.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
