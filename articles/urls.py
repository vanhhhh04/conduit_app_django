from django.contrib import admin
from django.urls import path
from . import views 
urlpatterns = [
    path('articles', views.list_articles, name="list_articles"),
    path('articles/<slug:slug>', views.update_or_delete_article, name="update_article"),
    path('tags', views.list_tags, name="list_tags"),
    path('update_slug', views.check_slug, name="list_tags"),
    # path('articles/<slug:slug>/comments',  )
]
