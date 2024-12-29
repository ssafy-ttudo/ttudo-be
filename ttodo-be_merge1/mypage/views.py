from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from boards.models import Ttodo, TtodoLike
from accounts.models import User, UserList
from .serializers import TodoSerializer, LikedTodoSerializer, UserProfileSerializer, UserListSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    is_own_profile = user == request.user

    my_todos = Ttodo.objects.filter(user=user)
    liked_todos = Ttodo.objects.filter(likes__user=user)

    data = {
        'profile': {
            'nickname': user.nickname,
            'profile_img': user.profile_img,
            'social_type': user.social,
            'created_date': user.created_date,
            'todo_count': my_todos.count(),
        },
        'is_own_profile': is_own_profile,
        'my_todos': TodoSerializer(my_todos, many=True, context={'request': request}).data,
        'liked_todos': LikedTodoSerializer(liked_todos, many=True).data,
        'bookmarked_users': [
            {
                'id': friend.id,
                'nickname': friend.nickname,
                'profile_img': friend.profile_img,
                'todo_count': Ttodo.objects.filter(user=friend).count(),
                'latest_todo': TodoSerializer(
                    Ttodo.objects.filter(user=friend).first(),
                    context={'request': request}
                ).data if Ttodo.objects.filter(user=friend).exists() else None
            }
            for friend in user.friend_list.all()
        ] if is_own_profile else []
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
