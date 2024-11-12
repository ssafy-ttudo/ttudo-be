from .models import Ttodo, Comment
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ttodo
        fields = ('__all__')
        read_only_fields = ('user',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('ttodo','user')
        
class ArticleCommentSerializer(serializers.ModelSerializer):
    class CommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('__all__')
            
    comment_set = CommentSerializer(read_only=True, many=True)
    
    class Meta:
        model = Ttodo
        fields = ('__all__')
        read_only_fields = ('user',)
