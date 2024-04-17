from django.db import models
from users.models import User
# Create your models here.
class Article(models.Model):
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    body = models.TextField()
    createdAt = models.DateTimeField(null=False, blank=False)
    updatedAt = models.DateTimeField(null=False, blank=False)

class Comment(models.Model):

    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    body = models.TextField()

class Tag(models.Model):
    article = models.ManyToManyField(Article)
    tag_name = models.CharField(max_length=100)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
