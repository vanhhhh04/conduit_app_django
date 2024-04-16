from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import datetime
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email,password=None):
        if not email :
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.TextField()
    bio = models.TextField(null = True, blank=True)
    image = models.CharField(max_length=100, null = True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=datetime.datetime.now())


    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="follow_follower")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="follow_user")


