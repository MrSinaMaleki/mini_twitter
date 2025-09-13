from rest_framework import serializers
from tweets.models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tweet
        fields = ('id', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('author', 'created_at', 'updated_at')

