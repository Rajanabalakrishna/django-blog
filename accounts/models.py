import uuid
from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_token')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.user.username} - {self.token}"
    
