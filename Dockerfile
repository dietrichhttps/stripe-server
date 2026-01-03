FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy and make entrypoint script executable
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Collect static files (if needed)
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]
