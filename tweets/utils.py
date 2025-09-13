from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_new_tweet_ws(tweet):
    channel_layer = get_channel_layer()

    data = {
        "id": tweet.id,
        "author": tweet.author.username,
        "content": tweet.content,
        "created_at": str(tweet.created_at),
    }

    async_to_sync(channel_layer.group_send)(
        "timeline",
        {
            "type": "new_tweet",
            "tweet": data
        }
    )
