#!/bin/bash

# Development startup script for DailyDose MVP

echo "🚀 Starting DailyDose MVP Development Environment"
echo "================================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please configure it with your settings."
    echo "   - Set SENDGRID_API_KEY for email functionality"
    exit 1
fi

# Check if migrations have been run
if [ ! -f db.sqlite3 ]; then
    echo "📦 Setting up database..."
    python3 manage.py migrate

    echo "📝 Populating database with quotes..."
    python3 manage.py populate_quotes

    echo "👤 Creating superuser..."
    python3 manage.py createsuperuser
fi

# Check if Redis is running
if ! pgrep -x "redis-server" > /dev/null; then
    echo "⚠️  Redis is not running. Celery tasks require Redis."
    echo "   Start Redis with: redis-server"
    echo ""
fi

echo ""
echo "✅ Starting Django development server..."
echo "   Access the application at: http://localhost:8000"
echo "   Admin panel: http://localhost:8000/admin/"
echo ""
echo "To enable background task processing:"
echo "  1. In a separate terminal, run: celery -A dailydose worker --loglevel=info"
echo "  2. In another terminal, run: celery -A dailydose beat --loglevel=info"
echo ""

python3 manage.py runserver
