from rest_framework import serializers
from .models import User 

# class Userserializer(serializers.ModelSerializer):

#     class Meta:
#         model = User 
#         fields = ["username","bio","image"]
class Userserializer(serializers.Serializer):
    username = serializers.CharField()
    bio = serializers.CharField()
    image = serializers.CharField()
    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return data
    


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length = 100, required=False)
    password = serializers.CharField(max_length = 100)
    bio = serializers.CharField(max_length = 100, required=False)
    image = serializers.CharField(max_length = 100, required = False)

    class Meta:
        model = User 
        fields = ["email","password"]