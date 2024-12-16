# restaurants/views.py
from django.shortcuts import render
from django.db.models import Min, Max
from .models import Restaurant, MenuItem
from .services import YelpService, GoogleMapsService, WeatherService

def restaurant_comparison_view(request):
    """
    Main view to compare restaurants and fetch comprehensive information
    """
    # Target restaurant (Village: Soul of India)
    target_restaurant_name = "Village: Soul of India"
    
    # Fetch target restaurant details from Yelp
    target_restaurant_data = YelpService.get_restaurant_details(target_restaurant_name)
    
    if not target_restaurant_data:
        return render(request, 'restaurants/error.html', {
            'error_message': 'Could not find the target restaurant'
        })
    
    # Extract key information
    latitude = target_restaurant_data['coordinates']['latitude']
    longitude = target_restaurant_data['coordinates']['longitude']
    
    # Fetch weather information
    weather_data = WeatherService.get_weather(latitude, longitude)
    
    # Find nearby restaurants
    nearby_restaurants = GoogleMapsService.find_nearby_restaurants(
        latitude, longitude, 
        keyword='restaurant'
    )
    
    # Prepare comparison data
    comparison_data = {
        'target_restaurant': {
            'name': target_restaurant_data['name'],
            'address': target_restaurant_data['location']['display_address'],
            'phone': target_restaurant_data['phone'],
            'rating': target_restaurant_data['rating'],
            'price': target_restaurant_data.get('price', 'N/A'),
            'open_now': target_restaurant_data.get('hours', [{}])[0].get('is_open_now', False)
        },
        'weather': {
            'temperature': weather_data['main']['temp'] if weather_data else 'N/A',
            'description': weather_data['weather'][0]['description'] if weather_data else 'N/A'
        },
        'nearby_restaurants': []
    }
    
    # Process nearby restaurants
    for restaurant in nearby_restaurants[:5]:  # Limit to top 5
        # Calculate distance from target restaurant
        distance = geodesic(
            (latitude, longitude), 
            (restaurant['geometry']['location']['lat'], restaurant['geometry']['location']['lng'])
        ).miles
        
        comparison_data['nearby_restaurants'].append({
            'name': restaurant['name'],
            'distance': round(distance, 2),
            'rating': restaurant.get('rating', 'N/A'),
            'price_level': restaurant.get('price_level', 'N/A')
        })
    
    return render(request, 'restaurants/comparison.html', comparison_data)
