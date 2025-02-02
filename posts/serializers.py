from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post

# Serializer for the User model to expose only non-sensitive fields like username and email
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # Excludes sensitive fields like 'password'


# Serializer for the Post model to handle all fields of the Post model
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # Exposes all fields by default, can be modified to specific fields
