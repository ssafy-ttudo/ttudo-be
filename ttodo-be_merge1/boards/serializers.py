from .models import Ttodo, Comment
from rest_framework import serializers
from django.utils.timezone import now

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ttodo
        fields = ('__all__')
        read_only_fields = ('user',)
        

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()  # 대댓글 목록 추가
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('ttodo','user')
        
    def get_replies(self, obj):
        # 현재 댓글(obj)에 연결된 대댓글 가져오기
        replies = Comment.objects.filter(parent_comment=obj)
        return CommentSerializer(replies, many=True, context=self.context).data
    
        
class ArticleCommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()  # like_count 메서드 추가
    comment_set = serializers.SerializerMethodField()  # 댓글 목록 포함
    class CommentSerializer(serializers.ModelSerializer):
        replies = serializers.SerializerMethodField()  # 대댓글 필드 추가
        class Meta:
            model = Comment
            fields = ('__all__')
            
    # comment_set = CommentSerializer(read_only=True, many=True)
    
    class Meta:
        model = Ttodo
        fields = ('__all__')
        read_only_fields = ('user',)
        
    def get_like_count(self, obj): # 좋아요 개수
        return obj.like_count()
    
    def get_comment_set(self, obj):
        # 최상위 댓글만 가져오기 (parent_comment가 None인 댓글)
        comments = Comment.objects.filter(ttodo=obj, parent_comment=None)
        return CommentSerializer(comments, many=True, context=self.context).data

class BoardSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()  # like_count 메서드 추가
    days_since_created = serializers.SerializerMethodField()
    recent_liked_user = serializers.SerializerMethodField()  # 최근 좋아요 유저
    
    class Meta:
        model = Ttodo
        fields = ('__all__')
        
    def get_days_since_created(self, obj): # 객체를 arguemnt로 받는다
        return (now() - obj.create_date).days # 이 메소드는 받은 객체를 직렬화해 원하는 형태로 변환해서 반환한다
    
    def get_like_count(self, obj): # 좋아요 개수
        return obj.like_count()
    
    def get_recent_liked_user(self, obj): # 가장 최근에 좋아요를 누른 유저
        recent_like = obj.likes.order_by('-created_at').first()  # 최신 순으로 정렬 후 첫 번째 객체 가져오기
        if recent_like:
            return recent_like.user.username  # 유저의 username 반환
        return None  # 좋아요가 없는 경우 None 반환