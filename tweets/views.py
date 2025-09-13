from django.db.models import Q
from rest_framework import viewsets, permissions, status
from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        tweet = self.get_object()
        user = request.user

        if user in tweet.likes.all():
            tweet.likes.remove(user)
            return Response({'detail': 'Unliked'}, status=status.HTTP_200_OK)
        else:
            tweet.likes.add(user)
            return Response({'detail': 'Liked'}, status=status.HTTP_200_OK)

    # ret-twwet
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def retweet(self, request, pk=None):
        tweet = self.get_object()
        new_tweet = Tweet.objects.create(
            author = request.user,
            original_tweet=tweet,
            content = tweet.content
        )
        serializer = self.get_serializer(new_tweet)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def timeline(self, request):
        user = request.user

        following_ids = user.following.values_list('following__id', flat=True)
        tweets = Tweet.objects.filter(
            Q(author__id__in=following_ids) | Q(author = user)
        ).order_by('-created_at')

        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

