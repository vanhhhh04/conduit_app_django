from rest_framework import serializers 
from .models import Article,Tag
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
            "body": {"required": False}
        }


        


