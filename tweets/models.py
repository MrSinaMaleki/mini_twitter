from django.db import models
from django.conf import settings

class TweetManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Tweet(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tweets')
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    original_tweet = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='retweets')

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_tweets', blank=True)

    objects = TweetManger()
    all_objects = TweetManger()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save(update_fields=['is_deleted'])

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"
