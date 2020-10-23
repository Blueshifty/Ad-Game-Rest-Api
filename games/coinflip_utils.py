import redis
import random
import uuid
from django.conf import settings
from .models import CoinFlipGame
import pickle
from celery import shared_task

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1, decode_responses=True)


def create_coinflip_game(user, name):
    if redis_instance.get(user.id):
        return False
    new_game = CoinFlipGame.objects.create(user=user, name=name)
    pickled_object = pickle.dumps(new_game)
    redis_instance.set(user.id, pickled_object)
    return True


'''
def join_coinflip_game(user, id):
'''