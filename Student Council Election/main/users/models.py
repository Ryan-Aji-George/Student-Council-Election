from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    HOUSE_CHOICES = [
        ('Unicorn', 'Unicorn'),
        ('Pegasus', 'Pegasus'),
        ('Phoenix', 'Phoenix'),
        ('Centaur', 'Centaur'),
        ('None', 'None'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One relation with User
    voter_name = models.CharField(max_length=200, default='') # Field for storing user's full name
    voter_class = models.CharField(max_length=200, default='')   
    house = models.CharField(max_length=10, choices=HOUSE_CHOICES, default='None')  # House field

    def __str__(self):
        return f"{self.voter_name} ({self.user.username})"