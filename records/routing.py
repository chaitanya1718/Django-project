from django.urls import re_path
from records import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
