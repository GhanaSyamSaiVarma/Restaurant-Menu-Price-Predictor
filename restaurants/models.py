# restaurants/models.py
from django.db import models
from django.utils import timezone

class Restaurant(models.Model):
    """Detailed restaurant model with comprehensive information"""
    name = models.CharField(max_length=200)
    yelp_id = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    rating = models.FloatField(null=True, blank=True)
    review_count = models.IntegerField(default=0)
    price_range = models.CharField(max_length=10, blank=True, null=True)
    
    # Operational details
    is_closed = models.BooleanField(default=False)
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    """Detailed menu item model"""
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class WeatherData(models.Model):
    """Model to store weather information for restaurant location"""
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    temperature = models.FloatField()
    feels_like = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather for {self.restaurant.name}"