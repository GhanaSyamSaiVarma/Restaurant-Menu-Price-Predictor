# restaurants/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('compare/', views.restaurant_comparison_view, name='restaurant_comparison'),
]