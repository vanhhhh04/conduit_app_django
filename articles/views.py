from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Article,Tag

from .serializers import ArticleSerializer, CommentSerializer
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
                article.update_slug() 
                article.save() 
                tagList = post_data.get("tagList",[])

                for tag_name in tagList:
                    tags = Tag.objects.filter(tag_name=tag_name)
                    if tags.exists() :
                        article.tags.add(*tags)  
                    else :
                        tag = Tag.objects.create(tag_name=tag_name)
                        article.tags.add(tag)
                print(serializer.data)
                serializer = serializer.data 
                serializer["tagList"] = tagList 
                
                
                return Response(serializer)
            else : 
                return Response(serializer.errors)
        return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def check_slug(request):
    if request.method == "GET":
        article = Article.objects.get(pk=1)
        print(article.update_slug())
        return Response("message")



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
            if request.user == article.author : 
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
    if request.method == "DELETE" :
        if request.user.is_authenticated :
            try :
                article = Article.objects.get(slug=slug)
            except Article.DoesNotExist:
                return Response({"error": "Article not found. "}, status = status.HTTP_400_BAD_REQUEST)
            if request.user == article.author :
                article.delete()
                return Response({"message":"deleted succesfully"})
            
                             
                



@api_view(["POST"])
def comment_views(request, slug):
    if request.method == "POST":
        if request.user.is_authenticated:
            try: 
                article = Article.objects.get(slug=slug)
            except Article.DoesNotExist:
                return Response({"message": "Article does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
            comment_post_data = request.data.get("comment")
            print(comment_post_data)
            comment_post_data = comment_post_data.get("body")
            print(comment_post_data)
            serializer = CommentSerializer(data=comment_post_data)
            
            if serializer.is_valid():
                serializer.save(article=article, author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


