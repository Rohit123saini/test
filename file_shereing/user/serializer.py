from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class loginserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields = ['username', 'password']

class OTPTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPToken
        fields = ('token',)

class fileserializer(serializers.ModelSerializer):
    class Meta:
        model=UploadedFile
        fields=['user','file']

    def validate_file(self, value):
        if not value.name.endswith(('.pptx', '.docx', '.xlsx')):
            raise serializers.ValidationError("Only .pptx, .docx, and .xlsx files are allowed.")
        return value