from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .forms import UserRegistrationForm, UserPreferenceForm, CustomPasswordResetForm
from .models import User, Quote, Category, UserQuoteHistory, UserPreference


def home(request):
    """Landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'quotes/home.html')


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('preferences')
    else:
        form = UserRegistrationForm()

    return render(request, 'quotes/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'quotes/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard showing recent quotes and stats"""
    recent_quotes = UserQuoteHistory.objects.filter(user=request.user)[:10]
    favorite_quotes = UserQuoteHistory.objects.filter(user=request.user, is_favorite=True)[:5]
    total_quotes_received = UserQuoteHistory.objects.filter(user=request.user).count()

    context = {
        'recent_quotes': recent_quotes,
        'favorite_quotes': favorite_quotes,
        'total_quotes_received': total_quotes_received,
        'user': request.user,
    }
    return render(request, 'quotes/dashboard.html', context)


@login_required
def preferences(request):
    """User preferences management"""
    user_pref, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=user_pref)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your preferences have been updated!')
            if request.htmx:
                return render(request, 'quotes/partials/preferences_form.html', {'form': form})
            return redirect('dashboard')
    else:
        form = UserPreferenceForm(instance=user_pref)

    return render(request, 'quotes/preferences.html', {'form': form})


@login_required
def quote_history(request):
    """View all received quotes"""
    quotes = UserQuoteHistory.objects.filter(user=request.user)
    return render(request, 'quotes/history.html', {'quotes': quotes})


@login_required
def toggle_favorite(request, history_id):
    """Toggle favorite status of a quote via HTMX"""
    history = get_object_or_404(UserQuoteHistory, id=history_id, user=request.user)
    history.is_favorite = not history.is_favorite
    history.save()

    if request.htmx:
        return render(request, 'quotes/partials/favorite_button.html', {'history': history})

    return redirect('quote_history')


@login_required
def favorites(request):
    """View all favorite quotes"""
    favorite_quotes = UserQuoteHistory.objects.filter(user=request.user, is_favorite=True)
    return render(request, 'quotes/favorites.html', {'quotes': favorite_quotes})


class CustomPasswordResetView(PasswordResetView):
    """Custom password reset view"""
    form_class = CustomPasswordResetForm
    template_name = 'quotes/password_reset.html'
    email_template_name = 'quotes/password_reset_email.html'
    success_url = '/password-reset/done/'


@login_required
def admin_analytics(request):
    """Admin analytics dashboard"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_quotes = Quote.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()
    total_sent = UserQuoteHistory.objects.count()

    # Category popularity
    popular_categories = Category.objects.annotate(
        quote_count=Count('quotes')
    ).order_by('-quote_count')[:5]

    # Recent activity
    recent_deliveries = UserQuoteHistory.objects.select_related('user', 'quote')[:10]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_quotes': total_quotes,
        'total_categories': total_categories,
        'total_sent': total_sent,
        'popular_categories': popular_categories,
        'recent_deliveries': recent_deliveries,
    }
    return render(request, 'quotes/admin_analytics.html', context)
