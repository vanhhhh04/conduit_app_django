from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('articles', views.list_articles, name="list_articles"),
    path('tags', views.list_tags, name="list_tags"),
]
