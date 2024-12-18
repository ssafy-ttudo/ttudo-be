from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category, Ttodo, Comment, Is_complete, CommentLike
from .serializers import ArticleSerializer, CommentSerializer, ArticleCommentSerializer,BoardSerializer
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.paginator import Paginator


# Create your views here.

# ttodo 메인 페이지
@api_view(['GET'])
@permission_classes([AllowAny])
def main(request):
    page = request.GET.get("page")
    articles = Ttodo.objects.all()
    serializer = BoardSerializer(articles, many=True)
    paginator = Paginator(serializer.data, 6)
    posts = paginator.get_page(page)
    return Response(posts.object_list)

# 카테고리 메인 페이지
@api_view(['GET'])
@permission_classes([AllowAny])
def category_main(request, category_name):
    page = request.GET.get("page")
    category_articles = Ttodo.objects.filter(category_name=category_name)
    serializer = BoardSerializer(category_articles, many=True)
    paginator = Paginator(serializer.data, 6)
    articles = paginator.get_page(page)
    return Response(articles.object_list)


# 게시글 crud
@api_view(['POST'])
@permission_classes([AllowAny])
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # serializer.save()
        serializer.save(user=request.user)
        
        return Response(serializer.data)
        

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def article_detail_update_delete(request, article_pk):
    article = Ttodo.objects.get(pk=article_pk)
    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        article.increment_views()  # 조회수 1 증가
        serializer = ArticleCommentSerializer(article)
        return Response(serializer.data)
    

# 댓글 crud
@api_view(['POST'])
@permission_classes([AllowAny])
def comment_create(request,article_pk):
    article = Ttodo.objects.get(pk=article_pk)
    parent_comment_id = request.data.get('parent_comment')  # 요청에서 parent_comment ID를 가져옴
    parent_comment = None
    
    if parent_comment_id:
        parent_comment = Comment.objects.get(pk=parent_comment_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(ttodo=article, parent_comment=parent_comment, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([AllowAny])
def comment_detail_update_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        
    elif request.method == 'GET':
        # 단일 댓글 직렬화
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def comment_reply(request, article_pk, comment_pk):
#     article = Ttodo.objects.get(pk=article_pk)
#     parent_comment = Comment.objects.get(pk=comment_pk)
#     serializer = CommentSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         # serializer.save(ttodo=article, user=request.user, parent_comment=parent_comment)
#         serializer.save(ttodo=article, parent_comment=parent_comment)
        
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    # 좋아요가 이미 눌려 있는지 확인
    existing_like = CommentLike.objects.filter(comment=comment, user=request.user)

    if existing_like.exists():
        # 이미 눌려 있다면 좋아요 취소
        existing_like.delete()
        return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
    else:
        # 좋아요 추가
        CommentLike.objects.create(comment=comment, user=request.user)
        return Response({"message": "Like added"}, status=status.HTTP_201_CREATED)


# 달성여부 체크

@api_view(['POST'])
@permission_classes([AllowAny])
def is_complete(request, article_pk):
    try:
        ttodo = Ttodo.objects.get(id=article_pk)  # 해당 게시글 찾기
    except Ttodo.DoesNotExist:
        return Response({'error': 'Ttodo not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    # Is_complete에 이미 데이터가 있는지 확인
    # is_complete, created = Is_complete.objects.get_or_create(user=user, ttodo=ttodo)
    is_complete, created = Is_complete.objects.get_or_create(user=user, ttodo=ttodo)
    

    if not created:
        # 이미 달성 상태라면 삭제 (달성 취소)
        is_complete.delete()
        return Response({'message': 'Todo marked as incomplete'}, status=status.HTTP_200_OK)
    else:
        # 달성 상태 추가
        return Response({'message': 'Todo marked as complete'}, status=status.HTTP_201_CREATED)