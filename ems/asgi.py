import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ems.settings")
django.setup()

from records.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 👈 Add this line to support normal web browsing
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
