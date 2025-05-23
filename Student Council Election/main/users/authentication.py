from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileCreatingBackend(ModelBackend):
    """Allows users to log in even if they don't have a profile. Creates one after login."""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user:
            # Ensure the user has a profile after successful login
            Profile.objects.get_or_create(user=user)
        return user