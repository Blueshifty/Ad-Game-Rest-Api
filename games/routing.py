from django.urls import path
from . import coinflip_consumers

websocket_urlpatterns = [
    path('coinflip-game/<str:game_name>/', coinflip_consumers.CoinFlipConsumer)
]
