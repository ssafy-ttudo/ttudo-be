from django.db import models
from django.conf import settings
from mypage.models import TtodoLike

# Create your models here.
class Category(models.Model):
	category_name = models.CharField(max_length=20)

class Ttodo(models.Model):
    # category_choice = [
    #     ('learning', '학습'),
    #     ('exercise', '운동'),
    #     ('food', '음식'),
    #     ('lifestyle', '생활루틴'),
    #     ('celebrity', '셀럽'),
    #     ('etc', '기타'),    
    # ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    # category_name = models.CharField(max_length=20, choices=category_choice)
    category_name = models.CharField(max_length=20)    
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    # File_size = 
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)  # 조회수 필드 추가
    def achieved_count(self):
        return self.is_complete.count()  # Is_complete 모델의 related_name 사용
    
    def like_count(self):
        return self.likes.count()  # TtodoLike 모델의 related_name을 통해 좋아요 개수를 반환
    # def has_liked(self, user): # 특정 사용자가 좋아요를 눌렀는지 여부
    #     return self.likes.filter(user=user).exists()
    
    def increment_views(self): # 조회수 증가
        self.views += 1
        self.save(update_fields=['views'])  # views 필드만 업데이트
    
class Comment(models.Model):
    ttodo = models.ForeignKey(Ttodo, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE) 
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Is_complete(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complete_todos', null=True, blank=True)
    ttodo = models.ForeignKey('boards.Ttodo', on_delete=models.CASCADE, related_name='is_complete')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ttodo')