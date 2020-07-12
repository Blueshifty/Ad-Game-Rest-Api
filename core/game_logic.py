import redis
import quantumrandom
import random
import uuid
from django.conf import settings
from accounts.models import User
import time
from .models import Game

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
redis_instance.set_response_callback('GET', int)  # GET VALUES AS INT


def create_game():
    redis_instance.flushdb()
    new_game = Game.objects.create(game_state='S')
    users = User.objects.filter(is_superuser=False, is_active=True, is_staff=False)
    for user in users:
        # Save 22 Byte Per Value If You Use Bytes
        # But Harder To Decode Test And Find Out The Best
        redis_instance.set(str(user.id), 0)
    new_game.save()


def start_lotto():
    start_time = time.time()
    total_score = counter = 0
    all_keys = redis_instance.keys('*')
    game = Game.objects.last()
    if game.game_state is not 'S':
        raise Game.DoesNotExist
    for key in all_keys:
        total_score += redis_instance.get(key)
    # lucky_number = int(quantumrandom.randint(0, total_score))
    lucky_number = random.randint(0, total_score)
    print(f'Total Score: {total_score} Lucky_Number: {lucky_number}')
    for key in all_keys:
        counter += redis_instance.get(key)
        if counter >= lucky_number:
            winner = key
            break
    try:
        game.winner = User.objects.get(id=uuid.UUID(winner))
        print(game.winner)
    except User.DoesNotExist:
        raise Exception('WINNER ID IS NOT IN DATABASE, SOMETHING WENT WRONG')
    print(f'Execution Time: {int(time.time() - start_time)} Seconds.')


def get_redis_values():
    for key in redis_instance.keys('*'):
        print(f'User:{User.objects.get(id=key)} Point: {redis_instance.get(key)}')


def randomize_redis_values():
    for key in redis_instance.keys('*'):
        print(f'OLD: {key} Point: {redis_instance.get(key)}')
        value = int(random.randint(0, 200))
        print(f'VALUE: {value}')
        redis_instance.incr(key, value)
        print(f'NEW: {key} Point: {redis_instance.get(key)}')
        # print(type(redis_instance.get(key)))
        # redis_instance.set(key, int(redis_instance.get(key)) + 1)
