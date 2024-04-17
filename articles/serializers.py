from rest_framework import serializers 
from .models import Article 
from users.serializers import Userserializer



class ArticleSerializer(serializers.ModelSerializer):
    author = Userserializer(many = False, read_only=True) 

    class Meta : 
        model = Article
        fields = ["slug","title","description","body","createdAt","updatedAt","author"]



