from django.db import models
from django.conf import settings

# Create your models here.
# class Category(models.Model):
# 	category_name = models.CharField(max_length=20)

# class Ttodo(models.Model):
#     category_choice = [
#         ('learning', '학습'),
#         ('exercise', '운동'),
#         ('food', '음식'),
#         ('lifestyle', '생활루틴'),
#         ('celebrity', '셀럽'),
#         ('etc', '기타'),    
#     ]
    
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
#     category_name = models.CharField(max_length=20, choices=category_choice)    
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     image = models.ImageField(null=True, blank=True)
#     # File_size = 
#     create_date = models.DateTimeField(auto_now_add=True)
#     update_date = models.DateTimeField(auto_now=True)
    
# class Comment(models.Model):
#     ttodo = models.ForeignKey(Ttodo, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE) 
#     content = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


# ## 새로 추가한 모델 - 필요없지않나?
# # mypage/models.py

class TtodoLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_todos')
    ttodo = models.ForeignKey('boards.Ttodo', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ttodo')