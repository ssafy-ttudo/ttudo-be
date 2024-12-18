# mypage/serializers.py
from rest_framework import serializers
# from .models import TtodoLike
from boards.models import Ttodo, TtodoLike

class TodoSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Ttodo
        fields = ['id', 'title', 'content', 'category_name', 'create_date', 'is_liked']
        
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return TtodoLike.objects.filter(user=user, ttodo=obj).exists()

class LikedTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ttodo
        fields = ['id', 'title', 'content', 'category_name', 'create_date']