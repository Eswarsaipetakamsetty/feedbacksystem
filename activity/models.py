from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.action} at {self.timestamp}"
