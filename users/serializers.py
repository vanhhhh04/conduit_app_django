from rest_framework import serializers
from .models import User 

class Userserializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length = 100)
    password = serializers.CharField(max_length = 100)
    bio = serializers.CharField(max_length = 100, required=False)
    image = serializers.CharField(max_length = 100, required = False)

    class Meta:
        model = User 
        fields = ["email","password","username"]

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