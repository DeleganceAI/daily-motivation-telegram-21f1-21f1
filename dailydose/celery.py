import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailydose.settings')

app = Celery('dailydose')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat schedule for daily quote delivery
app.conf.beat_schedule = {
    'send-daily-quotes': {
        'task': 'quotes.tasks.send_daily_quotes',
        'schedule': crontab(minute=0, hour='*'),  # Run every hour to check user preferences
    },
}
