from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Quote, UserPreference, UserQuoteHistory


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'preferred_time', 'last_quote_sent', 'is_active']
    list_filter = ['is_active', 'is_staff', 'preferred_time']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Quote Preferences', {'fields': ('preferred_time', 'last_quote_sent')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'author', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['text', 'author']
    list_editable = ['is_active']

    def text_preview(self, obj):
        return obj.text[:75] + '...' if len(obj.text) > 75 else obj.text
    text_preview.short_description = 'Quote Text'


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'delivery_paused', 'get_categories', 'updated_at']
    list_filter = ['delivery_paused', 'preferred_categories']
    filter_horizontal = ['preferred_categories']
    search_fields = ['user__username', 'user__email']

    def get_categories(self, obj):
        return ', '.join([cat.name for cat in obj.preferred_categories.all()])
    get_categories.short_description = 'Preferred Categories'


@admin.register(UserQuoteHistory)
class UserQuoteHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'quote_preview', 'sent_at', 'is_favorite']
    list_filter = ['is_favorite', 'sent_at']
    search_fields = ['user__username', 'quote__text', 'quote__author']
    readonly_fields = ['sent_at']

    def quote_preview(self, obj):
        return obj.quote.text[:50] + '...' if len(obj.quote.text) > 50 else obj.quote.text
    quote_preview.short_description = 'Quote'
