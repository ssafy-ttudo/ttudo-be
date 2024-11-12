from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category, Ttodo, Comment
from .serializers import ArticleSerializer, CommentSerializer, ArticleCommentSerializer


# Create your views here.

# ttodo 메인 페이지
@api_view(['GET'])
def main(request):
    pass

# 카테고리 메인 페이지
@api_view(['GET'])
def category_main(request, category_name):
    category = Ttodo.objects.filter(category_name=category_name)
    serializer = ArticleSerializer(category, many=True)
    return Response(serializer.data)
# 몇 명이 담았는지




# 게시글 crud
@api_view(['POST'])
def article_create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
        

@api_view(['GET', 'DELETE', 'PUT'])
def article_detail_update_delete(request, article_pk):
    article = Ttodo.objects.get(pk=article_pk)
    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        serializer = ArticleCommentSerializer(article)
        return Response(serializer.data)
    

# 댓글 crud
@api_view(['POST'])
def comment_create(request,article_pk):
    article = Ttodo.objects.get(pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(ttodo=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail_update_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'GET':
        # 단일 댓글 직렬화
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)