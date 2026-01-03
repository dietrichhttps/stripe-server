#!/bin/bash
set -e

# Ensure database file is writable
if [ -f /app/db.sqlite3 ]; then
    chmod 666 /app/db.sqlite3 || true
fi

# Run migrations
python manage.py migrate --noinput

# Start server
exec python manage.py runserver 0.0.0.0:8000
