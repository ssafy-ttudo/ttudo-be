from rest_framework import serializers
from .models import User, UserList

# 유저 정보 시리얼라이저
class UserInfoSerializer(serializers.ModelSerializer):
    class FriendSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = (
                'id',
                'nickname',
                'profile_img',
            )
            
    friends = FriendSerializer(many=True, read_only=True)
    friend_count = serializers.IntegerField(source='friends.count', read_only=True)
        
    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'social',
            'profile_img',
            'friends',
            'friend_count',
        )
        
# 유저에게 뜨는 다른 모든 유저 목록
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'social_id',
            'nickname',
            'profile_img',
        )
        
# 