from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import User
from .serializers import Userserializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status 
# Create your views here.

    
@api_view(["POST"])
def user_register(request):
    if request.method == "POST":
        user_info = request.data.get("user")
        serializer = Userserializer(data=user_info)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            bio = serializer.validated_data.get('bio')
            image = serializer.validated_data.get('bio')
            user = User.objects.create(username = username, email=email,bio=bio, image=image)
            user.set_password(password)
            user.save()
            response = {"user" : { 
                    "email":user.email,
                    "token": Token.objects.create(user=user).key,
                    "username":user.username,
                    "bio":user.bio,
                    "image":user.image
                     }
                }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=400)

@api_view(['POST'])
def user_login(request):
    if request.method == "POST":
        user_info = request.data.get("user")
        serializer = UserLoginSerializer(data = user_info)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Doesnot exist!"
                }
            }
            email = serializer.validated_data.get('email') 
            password = serializer.validated_data.get('password')
            user = User.objects.get(email=email) 
            if user.check_password(password) :
                token, created = Token.objects.get_or_create(user=user)
                # print(Token.objects.get_or_create(user=user))
                response = {"user" : { 
                    "email":user.email,
                    "token": token.key,
                    "username":user.username,
                    "bio":user.bio,
                    "image":user.image
                     }
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_or_update_user(request):
    if request.method == "GET":
        if request.user.is_authenticated : 
            user = request.user
            print(type(request.user))
            response = {"user" : { 
                    "email":user.email,
                    "username":user.username,
                    "bio":user.bio,
                    "image":user.image
                    }
                }
            return Response(response, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        if request.user.is_authenticated :
            update_data = request.data 
            serializer = UserLoginSerializer(data = update_data)
            user = User.objects.update()


@api_view([''])
def get_profile(request):
    pass 