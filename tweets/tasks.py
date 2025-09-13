from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_tweet_email(author_username, tweet_content, recipient_list):
    for email in recipient_list:
        send_mail(
            subject=f"New tweet from {author_username}",
            message=f"{author_username} tweeted:\n\n{tweet_content}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

