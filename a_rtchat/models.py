from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}: {self.message}'

    class Meta:
        ordering = ['-created_at']