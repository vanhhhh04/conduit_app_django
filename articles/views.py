from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Article,Tag

from .serializers import ArticleSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status 
# Create your views here.



@api_view(["GET","POST"])
def list_articles(request):
    if request.method == "GET":
        list_articles = Article.objects.all()
        serializer = ArticleSerializer(list_articles, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        if request.user.is_authenticated:
            post_data = request.data.get("article")
            serializer = ArticleSerializer(data = post_data)
            if serializer.is_valid() : 
                # title = serializer.validated_data("title")
                # description = serializer.validated_data("description")
                # body = serializer.validated_data("body")
                article = serializer.save()
                article.author = request.user 
                article.save()
                tagList = post_data.get("tagList",[])

                for tag_name in tagList:
                    tags = Tag.objects.filter(tag_name=tag_name)
                    if tags.exists() :
                        article.tags.add(*tags)  
                    else :
                        tag = Tag.objects.create(tag_name=tag_name)
                        article.tags.add(tag)
                serializer = serializer.data 
                serializer["tagList"] = tagList
                
                return Response(serializer)
            else : 
                return Response(serializer.errors)
        return Response(status = status.HTTP_400_BAD_REQUEST)





@api_view(["GET"])
def list_tags(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        list_tag = []
        for i in tags :
            list_tag.append(i.tag_name)
        response = {
            "tags": list_tag
        }
        return Response(response)
@api_view(["PUT"])
def update_or_delete_article(request, slug):
    if request.method == "PUT":
        if request.user.is_authenticated : 
            try:
                article = Article.objects.get(slug=slug)
            except Article.DoesNotExist:
                return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)
            put_data = request.data.get("article")
            serializer = ArticleSerializer(article, put_data)
            if serializer.is_valid():
                article = serializer.save()
                tagList = []
                tags = article.tags.all()
                print(type(tags))
                for i in tags :
                    print(i)
                    tagList.append(i.tag_name)
                serializer = serializer.data 
                serializer["tagList"] = tagList 
                return Response(serializer)
            else :
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        if request.user.is_authenticated : 
            


