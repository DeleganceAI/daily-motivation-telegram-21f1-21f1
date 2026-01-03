# DailyDose MVP - Setup Guide

## Overview

DailyDose is a Django-based web application that delivers personalized motivational quotes to users via email. The MVP includes user authentication, preference management, quote history tracking, and automated daily delivery via Celery.

## Tech Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5 + HTMX for dynamic interactions
- **Database**: SQLite (development) / PostgreSQL (production)
- **Task Queue**: Celery + Redis
- **Email**: SendGrid API

## Prerequisites

- Python 3.11+
- Redis (for Celery)
- SendGrid API key (for email delivery)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd dailydose
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 4. Database Setup

Run migrations to create the database:

```bash
python manage.py migrate
```

### 5. Populate Database with Quotes

Load 100 motivational quotes into the database:

```bash
python manage.py populate_quotes
```

### 6. Create Superuser

Create an admin account:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

## Running the Application

### 1. Start the Django development server

```bash
python manage.py runserver
```

Access the application at: http://localhost:8000

### 2. Start Redis (in a separate terminal)

```bash
redis-server
```

### 3. Start Celery Worker (in a separate terminal)

```bash
celery -A dailydose worker --loglevel=info
```

### 4. Start Celery Beat (in a separate terminal)

```bash
celery -A dailydose beat --loglevel=info
```

## Features

### User Features

1. **User Registration & Authentication**
   - Register with email and password
   - Login/logout functionality
   - Password reset via email

2. **Dashboard**
   - View recent quotes received
   - See favorite quotes
   - Track total quotes received

3. **Preferences Management**
   - Set preferred delivery time (UTC)
   - Select favorite quote categories
   - Pause/resume daily delivery

4. **Quote History**
   - View all received quotes
   - Mark quotes as favorites (HTMX-powered)
   - Filter by date and category

5. **Favorites**
   - Save favorite quotes
   - Quick access to inspirational content

### Admin Features

1. **Admin Panel** (http://localhost:8000/admin/)
   - Manage users, quotes, and categories
   - View quote history
   - Configure user preferences

2. **Analytics Dashboard** (http://localhost:8000/analytics/)
   - Total users and active users
   - Quote statistics
   - Popular categories
   - Recent deliveries

### Daily Quote Delivery

- Automated email delivery via Celery Beat
- Runs hourly to check user preferences
- Sends quotes at user's preferred time
- No duplicates within 30 days
- Respects category preferences

## Project Structure

```
dailydose/
├── dailydose/              # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py            # Root URL configuration
│   ├── celery.py          # Celery configuration
│   └── wsgi.py            # WSGI application
├── quotes/                 # Main application
│   ├── models.py          # Data models
│   ├── views.py           # View logic
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   ├── tasks.py           # Celery tasks
│   ├── urls.py            # App URL configuration
│   └── management/        # Custom commands
│       └── commands/
│           └── populate_quotes.py
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   └── quotes/           # App templates
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
├── manage.py            # Django management script
└── README.md            # Project documentation
```

## Data Models

### User (Extended Django User)
- Custom user model with `preferred_time` and `last_quote_sent` fields
- Manages authentication and quote delivery preferences

### Category
- Organizes quotes by themes (Success, Resilience, Growth, etc.)
- Used for user preference filtering

### Quote
- Stores quote text, author, and category
- Active/inactive flag for content management

### UserPreference
- One-to-one with User
- Stores preferred categories and delivery pause status

### UserQuoteHistory
- Tracks sent quotes and favorites
- Prevents duplicates within 30 days
- Supports favorite marking

## API Endpoints

### Public Routes
- `/` - Landing page
- `/register/` - User registration
- `/login/` - User login
- `/password-reset/` - Password reset flow

### Authenticated Routes
- `/dashboard/` - User dashboard
- `/preferences/` - Manage preferences
- `/history/` - View quote history
- `/favorites/` - View favorite quotes
- `/toggle-favorite/<id>/` - Toggle favorite (HTMX)

### Admin Routes
- `/admin/` - Django admin panel
- `/analytics/` - Analytics dashboard (staff only)

## Testing

Run Django's built-in tests:

```bash
python manage.py test
```

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure a production database (PostgreSQL recommended)
3. Set up proper email service credentials
4. Use a production WSGI server (Gunicorn included)
5. Configure Redis for production
6. Set up supervisor/systemd for Celery workers
7. Use a reverse proxy (Nginx/Apache)
8. Configure SSL certificates

### Example Gunicorn command:

```bash
gunicorn dailydose.wsgi:application --bind 0.0.0.0:8000
```

## Troubleshooting

### Email not sending
- Verify SendGrid API key in `.env`
- Check Celery worker logs
- Ensure Redis is running

### Celery tasks not running
- Verify Redis connection
- Check Celery worker and beat are running
- Review Celery logs for errors

### Database errors
- Run migrations: `python manage.py migrate`
- Check database file permissions (SQLite)

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| SECRET_KEY | Django secret key | Yes | - |
| DEBUG | Debug mode | No | True |
| ALLOWED_HOSTS | Allowed host names | No | localhost,127.0.0.1 |
| SENDGRID_API_KEY | SendGrid API key | Yes | - |
| DEFAULT_FROM_EMAIL | From email address | No | noreply@dailydose.com |
| CELERY_BROKER_URL | Redis URL for Celery | No | redis://localhost:6379/0 |
| CELERY_RESULT_BACKEND | Result backend URL | No | redis://localhost:6379/0 |

## Future Enhancements (Post-MVP)

- Mobile app integration
- SMS delivery option
- AI-powered quote recommendations
- User-generated content
- Social sharing features
- Multi-language support
- Advanced analytics
- Premium subscription features

## Support

For issues or questions, please refer to the documentation or contact the development team.

## License

Proprietary - All rights reserved
