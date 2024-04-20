from django.db import models
from users.models import User
import datetime 
# Create your models here.
class Article(models.Model):
    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,unique=False)
    slug = models.SlugField(null = True,blank = True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    body = models.TextField()
    createdAt = models.DateTimeField(null=False, blank=False, auto_now_add=datetime.datetime.now())
    updatedAt = models.DateTimeField(null=False, blank=False, auto_now_add=datetime.datetime.now())
    def update_slug(self):
        if not self.slug :
            slug = ""
            title_list = self.title.split(" ")

            for i in range(len(title_list)):
                slug += title_list[i]
                if i != len(title_list) - 1 : 
                    slug += "-"
            
            self.slug = slug  
            self.save()

class Comment(models.Model):

    author = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()
    body = models.TextField()

class Tag(models.Model):
    article = models.ManyToManyField(Article, related_name="tags")
    tag_name = models.CharField(max_length=100)



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
