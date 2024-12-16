# mypage/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import User, UserList
from boards.models import Ttodo
from .models import TtodoLike
from .serializers import TodoSerializer, LikedTodoSerializer, UserProfileSerializer, UserListSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mypage_view(request):
    user = request.user
    
    my_todos = Ttodo.objects.filter(user=user)
    liked_todos = Ttodo.objects.filter(likes__user=user).select_related('user')
    
    data = {
        'profile': UserProfileSerializer(user, context={'request': request}).data,
        'my_todos': TodoSerializer(my_todos, many=True, context={'request': request}).data,
        'liked_todos': LikedTodoSerializer(liked_todos, many=True).data,
    }
    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = User.objects.all().exclude(id=request.user.id)
    serializer = UserListSerializer(users, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_unfollow(request):
    friend_id = request.data.get('friend_id')
    if not friend_id:
        return Response({'error': 'Friend_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        friend = User.objects.get(id=friend_id)
    except User.DoesNotExist:
        return Response({'error':'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    friendship, created = UserList.objects.get_or_create(user=request.user, friend=friend)
    
    if created:
        return Response({'message':'Friend added successfully.'}, status=status.HTTP_201_CREATED)
    else:
        friendship.delete()
        return Response({'message':'Friend removed successfully.'}, status=status.HTTP_200_OK)
