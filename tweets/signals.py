from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from tweets.models import Tweet
from .tasks import send_tweet_email


@receiver(post_save, sender=Tweet)
def send_email_to_followers(sender, instance, created, **kwargs):
    if created and instance.original_tweet is None:
        author = instance.author
        followers_emails = list(author.followers.values_list('follower__email', flat=True))
        if followers_emails:
            send_tweet_email.delay(author.username, instance.content, followers_emails)


