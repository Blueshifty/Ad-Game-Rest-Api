import json
import random
from channels.generic.websocket import WebsocketConsumer
from .models import *
from .coinflip_utils import *

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, decode_responses=True)

class CoinFlipConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous or self.scope['kwargs']['game_name'] is None:
            self.close()
        else:
            print(self.scope['user'])
            self.accept()

    def disconnect(self, code):
        if self.game.creator is self.scope["user"]:
            self.channel_layer.group_discard(
                self.game_group_name,
                self.channel_name
            )
        else:
            self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'message',
                    'message': "Visitor Just Left The Game."
                }
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message == 'create':
            create_coinflip_game(user=self.scope['user'], name=text_data_json['name'])
            message = "Game Has Been Created"
        else:
            if CoinFlipGame.objects.get(id=self.scope['url_route']['kwargs']['id']) is None:
                message = f'{self.scope["user"]} Has Been Joined Game'
            self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'message',
                    'message': message
                }
            )
            self.channel_layer.group_add(
                self.game_group_name,
                self.channel_name
            )


        # Send message to room group
        # Start The Game When Both Agree To Play :)




        self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user.user_name}: {message}',
            }
        )
