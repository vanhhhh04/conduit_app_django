from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Article,Tag

from .serializers import ArticleSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status 
# Create your views here.



@api_view(["GET"])
def list_articles(request):
    if request.method == "GET":
        list_articles = Article.objects.all()
        serializer = ArticleSerializer(list_articles, many=True,)
        return Response(serializer.data)
    if request.method == "POST":
        post_data = request.data.get("article")
        pass 

@api_view(["GET"])
def list_tags(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        list_tag = []
        for i in tags :
            list_tag.append(i.tag_name)
        response = {
            "tags":list_tag
        }
        return Response(response)
