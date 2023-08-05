from rest_framework import serializers

from base.serializer import UserSerializer
from .models import posts

class PostSerializer(serializers.ModelSerializer):
    post_author = UserSerializer(read_only = True)
    
    class Meta:
        Model = posts
        fields = ('body','image','post_author','created_time','')