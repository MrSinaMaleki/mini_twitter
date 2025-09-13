from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/timeline/", consumers.TimelineConsumer.as_asgi()),
]
