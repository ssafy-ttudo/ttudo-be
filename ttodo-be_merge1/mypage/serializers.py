# mypage/serializers.py
from rest_framework import serializers
from accounts.models import User
from boards.models import Ttodo
from .models import TtodoLike

class TodoSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Ttodo
        fields = ['id', 'title', 'content', 'category_name', 'create_date', 'is_liked']
        
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return TtodoLike.objects.filter(user=user, ttodo=obj).exists()

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile_img']

class LikedTodoSerializer(serializers.ModelSerializer):
    author = UserBriefSerializer(source='user', read_only=True)

    class Meta:
        model = Ttodo
        fields = ['id', 'title', 'content', 'category_name', 'create_date', 'author']

class FriendSerializer(serializers.ModelSerializer):
    todo_count = serializers.SerializerMethodField()
    latest_todo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'nickname', 'profile_img', 'todo_count', 'latest_todo')

    def get_todo_count(self, obj):
        return Ttodo.objects.filter(user=obj).count()

    def get_latest_todo(self, obj):
        latest_todo = Ttodo.objects.filter(user=obj).order_by('-create_date').first()
        if latest_todo:
            return TodoSerializer(latest_todo, context=self.context).data
        return None

class UserProfileSerializer(serializers.ModelSerializer):
    todo_count = serializers.SerializerMethodField()
    bookmarked_users = FriendSerializer(source='friend_list', many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'profile_img',
            'social',
            'created_date',
            'todo_count',
            'bookmarked_users',
        )

    def get_todo_count(self, obj):
        return Ttodo.objects.filter(user=obj).count()

class UserListSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'social_id', 'nickname', 'profile_img', 'is_following')

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.friend_list.filter(id=obj.id).exists()
        return False
