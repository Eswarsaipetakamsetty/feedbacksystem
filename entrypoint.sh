#!/bin/bash

# Exit the script on any error
set -e

echo "⏳ Waiting for PostgreSQL to be ready..."
until nc -z db 5432; do
  sleep 0.5
done

echo "✅ PostgreSQL is available. Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🚀 Starting Django server..."
exec "$@"
