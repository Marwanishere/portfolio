from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user1")
    title = models.CharField(max_length=64)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default = 0)
    liked = models.BooleanField(default = False)

    def serialize(self):
        return {
            "user": self.user.username,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp.strftime('%B %d, %Y, %I:%M %p'),
            "likes": self.likes,
            "liked": self.liked,
        }
    # cs50 chatbot helped with making the different variables in the self serialize function

class FS(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "follower", default = False)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "following", default = False)