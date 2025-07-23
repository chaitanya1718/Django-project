import os
import django
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ems.settings")
# django.setup()

import records.routing 

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  
     "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(records.routing.websocket_urlpatterns))
    ),
})
