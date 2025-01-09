from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    profile_img = models.URLField()
    social_id = models.CharField(max_length=200, unique=True)
    social = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    friend_list = models.ManyToManyField('self', through='UserList', symmetrical=False, related_name='friends')
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    jwt_access_token = models.TextField(blank=True, null=True)
    jwt_refresh_token = models.TextField(blank=True, null=True)

    def __str__(self):
        return super().__str__()
    
class UserList(models.Model):
    # 추가한 친구
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')
    
    # 나
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_users')