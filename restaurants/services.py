# restaurants/services.py
import os
import requests
from django.conf import settings
from dotenv import load_dotenv
from geopy.distance import geodesic

# Load environment variables
load_dotenv()

class YelpService:
    """Service for interacting with Yelp Fusion API"""
    BASE_URL = 'https://api.yelp.com/v3/businesses'
    
    @classmethod
    def get_restaurant_details(cls, restaurant_name, location='Hicksville, NY'):
        """
        Fetch detailed restaurant information from Yelp
        :param restaurant_name: Name of the restaurant
        :param location: Location to search in
        :return: Dictionary of restaurant details
        """
        headers = {
            'Authorization': f'Bearer {os.getenv("YELP_API_KEY")}'
        }
        
        # Search for the business
        search_url = f'{cls.BASE_URL}/search'
        params = {
            'term': restaurant_name,
            'location': location,
            'limit': 1
        }
        
        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            businesses = response.json().get('businesses', [])
            
            if not businesses:
                return None
            
            # Get detailed business information
            business = businesses[0]
            business_id = business['id']
            
            # Fetch detailed business info
            business_url = f'{cls.BASE_URL}/{business_id}'
            business_response = requests.get(business_url, headers=headers)
            business_response.raise_for_status()
            
            return business_response.json()
        
        except requests.RequestException as e:
            print(f"Yelp API Error: {e}")
            return None

class GoogleMapsService:
    """Service for interacting with Google Maps API"""
    BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    
    @classmethod
    def find_nearby_restaurants(cls, latitude, longitude, radius=2000, keyword=None):
        """
        Find nearby restaurants using Google Places API
        :param latitude: Latitude of center point
        :param longitude: Longitude of center point
        :param radius: Search radius in meters (max 50000)
        :param keyword: Optional keyword to filter restaurants
        :return: List of nearby restaurants
        """
        params = {
            'location': f'{latitude},{longitude}',
            'radius': radius,
            'type': 'restaurant',
            'key': os.getenv('GOOGLE_MAPS_API_KEY')
        }
        
        if keyword:
            params['keyword'] = keyword
        
        try:
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return response.json().get('results', [])
        
        except requests.RequestException as e:
            print(f"Google Maps API Error: {e}")
            return []

class WeatherService:
    """Service for fetching weather information"""
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
    
    @classmethod
    def get_weather(cls, latitude, longitude):
        """
        Fetch current weather for given coordinates
        :param latitude: Latitude
        :param longitude: Longitude
        :return: Dictionary of weather information
        """
        params = {
            'lat': latitude,
            'lon': longitude,
            'appid': os.getenv('OPENWEATHER_API_KEY'),
            'units': 'imperial'  # Use Fahrenheit
        }
        
        try:
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.RequestException as e:
            print(f"OpenWeather API Error: {e}")
            return None