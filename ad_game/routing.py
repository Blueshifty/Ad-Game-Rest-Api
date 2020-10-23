from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from channels.routing import ProtocolTypeRouter
import core.routing
import games.routing
from .channelsmiddleware import JwtTokenAuthMiddleWareStack

application = ProtocolTypeRouter({
    'websocket': JwtTokenAuthMiddleWareStack(
        URLRouter(
            games.routing.websocket_urlpatterns
        ),
    ),
})
