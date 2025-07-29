import uuid
from django.db import models

from django.contrib.auth.hashers import make_password

# Create your models here.
class CustomUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):  # avoids double hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

        
    def __str__(self):
        return f"{self.username}"
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    short_intro = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/default.png')

    def __str__(self):
        return f"Profile of {self.user.username}"
    
class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.username}"