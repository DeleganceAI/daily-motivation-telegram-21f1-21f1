from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """Extended user model with additional fields for quote delivery"""
    preferred_time = models.TimeField(default='08:00:00', help_text='Time to receive daily quote (UTC)')
    is_active = models.BooleanField(default=True)
    last_quote_sent = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'


class Category(models.Model):
    """Quote categories for user preference selection"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Quote(models.Model):
    """Motivational quotes with author and category"""
    text = models.TextField()
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quotes')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text[:50]}... - {self.author}"


class UserPreference(models.Model):
    """User preferences for quote categories and delivery settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    preferred_categories = models.ManyToManyField(Category, blank=True)
    delivery_paused = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"


class UserQuoteHistory(models.Model):
    """Track which quotes have been sent to which users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quote_history')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='user_history')
    sent_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'User Quote Histories'
        ordering = ['-sent_at']
        unique_together = ['user', 'quote', 'sent_at']

    def __str__(self):
        return f"{self.user.username} - {self.quote.text[:30]}... - {self.sent_at.date()}"

    @classmethod
    def get_unsent_quote_for_user(cls, user):
        """Get a random quote that hasn't been sent to this user in the last 30 days"""
        thirty_days_ago = timezone.now() - timedelta(days=30)

        # Get user's preferred categories
        user_categories = user.preferences.preferred_categories.all()

        # If user has no preferences, use all categories
        if not user_categories.exists():
            quote_queryset = Quote.objects.filter(is_active=True)
        else:
            quote_queryset = Quote.objects.filter(is_active=True, category__in=user_categories)

        # Exclude quotes sent in the last 30 days
        recent_quote_ids = cls.objects.filter(
            user=user,
            sent_at__gte=thirty_days_ago
        ).values_list('quote_id', flat=True)

        quote_queryset = quote_queryset.exclude(id__in=recent_quote_ids)

        # Return random quote
        return quote_queryset.order_by('?').first()
