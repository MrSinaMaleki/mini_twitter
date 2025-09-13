
from rest_framework import viewsets, permissions
from tweets.models import Tweet
from tweets.serializers import TweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

