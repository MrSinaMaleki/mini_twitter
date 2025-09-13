from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from tweets.models import Tweet


@receiver(post_save, sender=Tweet)
def send_email_to_followers(sender, instance, created, **kwargs):
    if created and instance.original_tweet is None:
        author = instance.author
        followers = author.followers.values_list('follower__email', flat=True)
        for email in followers:
            send_mail(
                subject=f"New tweet from {author.username}",
                message=f"{author.username} tweeted:\n\n{instance.content}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

            print(f"Email sent to {email} for tweet '{instance.content[:30]}'")

