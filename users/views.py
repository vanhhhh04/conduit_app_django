from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import User
from .serializers import Userserializer,UserLogin
from rest_framework.authtoken.models import Token
from rest_framework import status 
# Create your views here.

    
@api_view(["POST"])
def user_register(request):
    if request.method == "POST":
        user_info = request.data.get("user")
        serializer = Userserializer(data=user_info)
        if serializer.is_valid():
            user = serializer.save()
            token,created=Token.objects.get_or_create(user=user)
            data_response = serializer.data 
            data_response['token'] = token.key 
            return Response({"user": data_response}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=400)
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



@api_view(['POST'])
def user_login(request):
    if request.method == "POST":
        user_info = request.data.get("user", {})
        email = user_info.get('email')
        password = user_info.get('password')

        if email is None or password is None:
            return Response({'detail': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        response = {
            "user": {
                "email": user.email,
                "token": token.key,
                "username": user.username,
                "bio": user.bio,
                "image": user.image
            }
        }
        return Response(response, status=status.HTTP_200_OK)
    
@api_view(['GET','PUT'])
def get_or_update_user(request):
    if request.method == "GET":
        if request.user.is_authenticated : 
            user = request.user
            token = Token.objects.get(user_id=user.id)
            print(user.__dict__.keys())
            response = {"user" : { 
                    "email":user.email,
                    "token": str(token),
                    "username":user.username,
                    "bio":user.bio,
                    "image":user.image
                    }
                }
            return Response(response, status=status.HTTP_200_OK)

    if request.method == "PUT":
        if request.user.is_authenticated:
            update_data = request.data["user"]
            user_name = update_data.get("user_name") 
            email = update_data.get("email") 
            print(update_data)
            if email:
                print(email)
                if email == request.user.email:
                    serializer = Userserializer(data=update_data, instance=request.user)
                    print(serializer)
                    if serializer.is_valid():
                        serialized_data = serializer.validated_data
                        print(serialized_data)  # Print the serialized data
                        serializer.save()   
                        return Response({"message": "yes"})
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else :
                    return Response({"message":"you are not allowed to change this information"})  

 
 
@api_view(['GET'])
def get_profile(request,username):
    if request.method == "GET":
        user_profile = User.objects.filter(username = username).exists()
        if user_profile :
            user_profile = User.objects.get(username = username)
            response = {
                "profile" : {
                    "username": user_profile.username, 
                    "bio": user_profile.bio, 
                    "image": user_profile.image, 
                    "following": False 
                } 
            } 
            return Response(response, status=status.HTTP_200_OK)
        response = {
                "username": {
                    "detail": "User Doesnot exist!"
                }
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
