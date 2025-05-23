import datetime
from django.utils import timezone
from django.db import models

class Post(models.Model):
    HOUSE_CHOICES = [
        ('Unicorn', 'Unicorn'),
        ('Pegasus', 'Pegasus'),
        ('Phoenix', 'Phoenix'),
        ('Centaur', 'Centaur'),
        ('None', 'Not a House Captain'),
    ]
    post_title = models.CharField(max_length=200)
    is_house_captain = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    house = models.CharField(max_length=10, choices=HOUSE_CHOICES, default='None')

    def __str__(self):
        return self.post_title


class Candidate(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    motto = models.CharField(max_length=300, default='')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.candidate_name

from django.contrib.auth.models import User

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # Ensures one vote per user per post

    def __str__(self):
        # Pull the voter’s display name from Profile
        try:
            voter_name = self.user.profile.voter_name
        except Profile.DoesNotExist:
            voter_name = self.user.username  # fallback

        # Use the Post’s title
        post_title = self.post.post_title

        return f"{voter_name} voted for {post_title}"

'''

Question = Post
question = post
choice_text = candidate_name
question_text = post_title
choice = candidate


'''