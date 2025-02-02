from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']  # Excludes sensitive fields like 'password'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'  # Or list specific fields like ['id', 'content', 'author', 'created_at']
