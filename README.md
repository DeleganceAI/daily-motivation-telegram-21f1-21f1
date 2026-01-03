# DailyDose - Daily Motivation Quotes

An Infinifab micro-SaaS project delivering personalized motivational quotes via email.

## Overview

DailyDose is a Django-based web application that sends daily motivational quotes to users based on their preferences. Users can register, choose their favorite quote categories, set delivery times, and track their quote history with favorites.

## Project Documentation

- [Design Document](docs/design.md) - Market research and business context
- [Technical Specification](docs/tech-spec.md) - MVP requirements and data models
- [Setup Guide](SETUP.md) - Complete installation and configuration instructions

## Features

✅ User registration and authentication with password reset
✅ Daily quote delivery via email (SendGrid)
✅ Category-based preferences (Success, Resilience, Growth, Courage, Mindfulness)
✅ Customizable delivery time
✅ Quote history tracking (no duplicates within 30 days)
✅ Favorite quotes with HTMX-powered toggling
✅ Admin analytics dashboard
✅ 100+ curated motivational quotes
✅ Celery-based scheduled tasks
✅ Bootstrap 5 responsive UI

## Tech Stack

- **Backend**: Django 4.2.7 with HTMX
- **Task Queue**: Celery + Redis
- **Email**: SendGrid
- **Frontend**: Bootstrap 5 + HTMX
- **Database**: SQLite (dev) / PostgreSQL (production ready)

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your SendGrid API key and other settings
```

### 3. Setup database

```bash
python manage.py migrate
python manage.py populate_quotes
python manage.py createsuperuser
```

### 4. Start services

**Option A: Using the dev script (recommended)**
```bash
./run_dev.sh
```

**Option B: Manual start**

Terminal 1 - Redis:
```bash
docker-compose up redis
# OR: redis-server
```

Terminal 2 - Django:
```bash
python manage.py runserver
```

Terminal 3 - Celery Worker:
```bash
celery -A dailydose worker --loglevel=info
```

Terminal 4 - Celery Beat:
```bash
celery -A dailydose beat --loglevel=info
```

### 5. Access the application

- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin/
- **Analytics**: http://localhost:8000/analytics/ (staff only)

## Project Structure

```
dailydose/
├── dailydose/          # Django project settings
├── quotes/             # Main application
│   ├── models.py       # Data models
│   ├── views.py        # Views and logic
│   ├── forms.py        # Django forms
│   ├── admin.py        # Admin interface
│   ├── tasks.py        # Celery tasks
│   └── management/     # Custom commands
├── templates/          # HTML templates
├── requirements.txt    # Dependencies
├── SETUP.md           # Detailed setup guide
└── run_dev.sh         # Development startup script
```

## MVP Completion Checklist

- ✅ REQ-1: User registration and authentication system
- ✅ REQ-2: Daily quote delivery system
- ✅ REQ-3: Quote database and curation (100+ quotes)
- ✅ REQ-4: User preference management
- ✅ REQ-5: Quote history and favorites
- ✅ REQ-6: Basic analytics dashboard

## Key Endpoints

- `/` - Landing page
- `/register/` - User registration
- `/login/` - User login
- `/dashboard/` - User dashboard
- `/preferences/` - Manage preferences
- `/history/` - View quote history
- `/favorites/` - View favorite quotes
- `/admin/` - Django admin panel
- `/analytics/` - Admin analytics

## Environment Variables

Key variables to configure in `.env`:

- `SECRET_KEY` - Django secret key
- `SENDGRID_API_KEY` - SendGrid API key for email delivery
- `DEFAULT_FROM_EMAIL` - From email address
- `CELERY_BROKER_URL` - Redis URL for Celery

See `.env.example` for complete list.

## Testing

```bash
python manage.py test
python manage.py check
```

## Production Deployment

See [SETUP.md](SETUP.md) for production deployment instructions including:
- Gunicorn configuration
- PostgreSQL setup
- Supervisor/systemd for Celery
- Nginx reverse proxy
- SSL configuration

---

*Built with [Infinifab](https://infinifab.com)*
