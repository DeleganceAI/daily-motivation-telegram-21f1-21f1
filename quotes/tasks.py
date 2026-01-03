from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from .models import User, UserQuoteHistory, UserPreference


@shared_task
def send_daily_quotes():
    """
    Celery task to send daily quotes to users based on their preferred time.
    This task runs every hour and checks which users should receive quotes.
    """
    current_time = timezone.now()
    current_hour = current_time.hour

    # Get all active users who haven't paused delivery
    users = User.objects.filter(is_active=True)

    sent_count = 0
    for user in users:
        # Check if user has preferences
        try:
            preferences = user.preferences
            if preferences.delivery_paused:
                continue
        except UserPreference.DoesNotExist:
            # Create default preferences
            UserPreference.objects.create(user=user)
            preferences = user.preferences

        # Check if it's time to send based on user's preferred time
        preferred_hour = user.preferred_time.hour
        if preferred_hour != current_hour:
            continue

        # Check if user already received a quote today
        today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        already_sent_today = UserQuoteHistory.objects.filter(
            user=user,
            sent_at__gte=today_start
        ).exists()

        if already_sent_today:
            continue

        # Get an unsent quote for this user
        quote = UserQuoteHistory.get_unsent_quote_for_user(user)

        if quote:
            # Send email with quote
            success = send_quote_email(user, quote)

            if success:
                # Record in history
                UserQuoteHistory.objects.create(user=user, quote=quote)

                # Update last_quote_sent timestamp
                user.last_quote_sent = current_time
                user.save()

                sent_count += 1

    return f"Sent {sent_count} quotes successfully"


def send_quote_email(user, quote):
    """
    Send a quote via email to a user
    """
    try:
        subject = 'Your Daily Motivation Quote'

        # Render HTML email
        html_message = render_to_string('quotes/email/daily_quote.html', {
            'user': user,
            'quote': quote,
        })

        # Plain text fallback
        plain_message = f"""
Hi {user.username},

Here's your daily motivation quote:

"{quote.text}"

- {quote.author}

Category: {quote.category.name}

Have a great day!

DailyDose Team
        """

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )

        return True
    except Exception as e:
        print(f"Failed to send email to {user.email}: {str(e)}")
        return False


@shared_task
def test_email_send(user_email):
    """Test task to verify email sending works"""
    try:
        send_mail(
            subject='Test Email from DailyDose',
            message='This is a test email to verify email configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return f"Test email sent to {user_email}"
    except Exception as e:
        return f"Failed to send test email: {str(e)}"
