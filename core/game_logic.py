import redis
import quantumrandom
import random
import uuid
from django.conf import settings
from accounts.models import User
from .models import Game
from .decorators import print_execution_time

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
redis_instance.set_response_callback('GET', int)  # GET VALUES AS INT
set_name = "Point-Table"


@print_execution_time
def create_game():
    redis_instance.flushdb()
    new_game = Game.objects.create(game_state='S')
    users = User.objects.filter(is_superuser=False, is_active=True, is_staff=False)
    for user in users:
        # Save 22 Byte Per Value If You Use Bytes
        # But Harder To Decode Test And Find Out The Best
        redis_instance.zadd(set_name, {str(user.id): 0})
        # redis_instance.set(str(user.id), 0)
    new_game.save()


@print_execution_time
def start_lotto():
    total_score = counter = 0
    game = Game.objects.last()
    if game.game_state is not 'S':
        raise Game.DoesNotExist
    print(
        f'{redis_instance.zremrangebyscore(set_name, 0, 1)} Users With 0 Point Deleted.')  # Remove all 0 point users from set.
    for value in redis_instance.zrange(set_name, 0, -1, withscores=True, desc=False):  # Randomizing Users For Lotto.
        total_score += int(value[1])
        redis_instance.set(value[0], int(value[1]))
        redis_instance.zrem(set_name, value[0])
    redis_instance.delete(set_name)  # Deleting Set, Dont Need it Anymore.
    # lucky_number = int(quantumrandom.randint(0, total_score))
    lucky_number = random.randint(0, total_score)
    print(f'Total Score: {total_score} Lucky_Number: {lucky_number}')
    for key in redis_instance.keys('*'):
        counter += redis_instance.get(key)
        if counter >= lucky_number:
            winner = key
            break
    try:
        game.winner = User.objects.get(id=uuid.UUID(winner))
        game.game_state = 'E'
        # game.save()
        print(game.winner)
    except User.DoesNotExist:
        raise Exception('WINNER ID IS NOT IN DATABASE, SOMETHING WENT WRONG')


@print_execution_time
def get_redis_values():
    for key in redis_instance.keys('*'):
        print(key)
        # print(f'User:{User.objects.get(id=key)} Point: {redis_instance.get(key)}')


@print_execution_time
def get_leader_board():
    for value in redis_instance.zrange(set_name, 0, -1, withscores=True, desc=True):
        print(value)

    '''
    print(redis_instance.client_getname())
    # redis_instance.sort(name=redis_instance.client_getname())
    
    for key in redis_instance.keys('*'):
        print(f'User:{key} Point: {redis_instance.get(key)}')
    '''


@print_execution_time
def randomize_redis_values():
    users = User.objects.filter(is_superuser=False, is_active=True, is_staff=False)
    for user in users:
        redis_instance.zincrby(set_name, int(random.randint(0, 200)), str(user.id))

    '''
    for key in redis_instance.keys('*'):
        print(f'OLD: {key} Point: {redis_instance.get(key)}')
        value = int(random.randint(0, 200))
        print(f'VALUE: {value}')
        redis_instance.zincrby(key, value)
        print(f'NEW: {key} Point: {redis_instance.get(key)}')
        # print(type(redis_instance.get(key)))
        # redis_instance.set(key, int(redis_instance.get(key)) + 1)
    '''
