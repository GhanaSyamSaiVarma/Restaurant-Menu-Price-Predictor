from django.apps import AppConfig

class RestaurantsConfig(AppConfig):
    """Configuration for the restaurants app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'

    def ready(self):
        """
        Add any app-specific initialization logic here.
        This method is called once when the app is loaded.
        """
        # You could import signals or perform other startup tasks here
        pass