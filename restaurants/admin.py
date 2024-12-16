from django.contrib import admin
from .models import Restaurant, MenuItem, WeatherData

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """Admin configuration for Restaurant model"""
    list_display = ('name', 'address', 'rating', 'price_range', 'is_closed', 'last_updated')
    search_fields = ('name', 'address')
    list_filter = ('is_closed', 'price_range')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin configuration for MenuItem model"""
    list_display = ('name', 'restaurant', 'price', 'category')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('restaurant', 'category')

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    """Admin configuration for WeatherData model"""
    list_display = ('restaurant', 'temperature', 'description', 'timestamp')
    list_filter = ('restaurant',)