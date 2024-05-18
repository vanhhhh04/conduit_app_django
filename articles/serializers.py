from rest_framework import serializers 
from .models import Article,Tag, Comment
from users.serializers import Userserializer



# class TagSerializer(serializers.ModelSerializer):
#     class Meta : 
#         model = Tag 
#         fields = [""]

class ArticleSerializer(serializers.ModelSerializer):
    author = Userserializer(many = False, read_only=True) 


    class Meta : 
        model = Article
        fields = ["slug","title","description","body","createdAt","updatedAt","author"]
        extra_kwargs = {
            "description": {"required": False},
            "body": {"required": False},
            "title": {"required": False}
        }
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "body", "createdAt", "updatedAt", "author"]
        read_only_fields = ["author", "createdAt", "updatedAt"]
        
    
        


