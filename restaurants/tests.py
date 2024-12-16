from django.test import TestCase
from django.utils import timezone
from .models import Restaurant, MenuItem, WeatherData
from .services import YelpService, GoogleMapsService, WeatherService

class RestaurantModelTests(TestCase):
    """Tests for Restaurant model"""
    def setUp(self):
        """Create a test restaurant"""
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            yelp_id="test-123",
            address="123 Test St",
            latitude=40.76678375818474,
            longitude=-74.0060,
            rating=4.5,
            price_range="$$"
        )

    def test_restaurant_creation(self):
        """Test restaurant model creation"""
        self.assertTrue(isinstance(self.restaurant, Restaurant))
        self.assertEqual(self.restaurant.__str__(), "Test Restaurant")

class YelpServiceTests(TestCase):
    """Tests for Yelp Service"""
    def test_get_restaurant_details(self):
        """Test retrieving restaurant details from Yelp"""
        restaurant_name = "Village: Soul of India"
        details = YelpService.get_restaurant_details(restaurant_name)
        
        # Basic validation
        self.assertIsNotNone(details)
        self.assertIn('name', details)
        self.assertIn('location', details)

class GoogleMapsServiceTests(TestCase):
    """Tests for Google Maps Service"""
    def test_find_nearby_restaurants(self):
        """Test finding nearby restaurants"""
        latitude, longitude = 40.76678375818474, -73.52366674602767
        nearby_restaurants = GoogleMapsService.find_nearby_restaurants(latitude, longitude)
        
        self.assertIsInstance(nearby_restaurants, list)
        self.assertTrue(len(nearby_restaurants) > 0)

class WeatherServiceTests(TestCase):
    """Tests for Weather Service"""
    def test_get_weather(self):
        """Test retrieving weather information"""
        latitude, longitude = 40.76678375818474, -73.52366674602767
        weather_data = WeatherService.get_weather(latitude, longitude)
        
        self.assertIsNotNone(weather_data)
        self.assertIn('main', weather_data)
        self.assertIn('weather', weather_data)