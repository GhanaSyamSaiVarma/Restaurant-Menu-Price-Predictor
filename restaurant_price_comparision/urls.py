from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),
    
    # Restaurants app URLs
    path('restaurants/', include('restaurants.urls')),
]