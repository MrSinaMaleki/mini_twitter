from rest_framework import serializers
from tweets.models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    retweets_count = serializers.SerializerMethodField()
    original_tweet = serializers.PrimaryKeyRelatedField(
        queryset=Tweet.objects.all(), required=False, allow_null=True
    )


    class Meta:
        model = Tweet
        fields = ('id', 'author', 'content', 'created_at', 'updated_at', 'original_tweet', 'likes_count', 'retweets_count')
        read_only_fields = ('author', 'created_at', 'updated_at', 'likes_count', 'retweets_count')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_retweets_count(self, obj):
        return obj.retweets.count()