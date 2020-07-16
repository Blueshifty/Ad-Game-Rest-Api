import redis
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from .models import Game
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from .game_logic import increment_user_point, create_game, randomize_redis_values, get_redis_values, start_lotto

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
redis_instance.set_response_callback('GET', int)  # GET VALUES AS INT
set_name = "Point-Table"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leader_board(request):
    top_20 = redis_instance.zrange(set_name, 0, -1, desc=True, withscores=True)[0:20]
    top_20_users = []
    for value in top_20:
        user = User.objects.get(id=value[0])
        top_20_users.append({"user_name": f'{user.first_name} {user.last_name}',
                             "user_avatar": user.avatar.url if user.avatar else None,
                             "user_score": int(value[1]),
                             "user_sex": user.sex,
                             })
    user_score = int(redis_instance.zscore(set_name, str(request.user.id)))
    user_rank = redis_instance.zrevrank(set_name, str(request.user.id))
    return Response(
        data={
            "top_20": top_20_users,
            "user_score": {"rank": user_rank + 1, "user_score": user_score}
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_point(request):
    #create_game.delay(add_users=True)
    #randomize_redis_values.delay()
    #start_lotto.delay()
    increment_user_point.delay(request.user.id)
    # redis_instance.zincrby(set_name, 1, str(request.user.id))
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_previous_games(request):
    finished_games = Game.objects.filter(game_state='E')
    games = []
    for game in finished_games:
        games.append({"date": game.date,
                      "winner": f'{game.winner.first_name} {game.winner.last_name}',
                      "winner-profile": None,
                      "total_point": game.total_point,
                      "winner-point": game.winner_point if game.winner_point else None})
    return Response(
        data={"games": games},
        status=status.HTTP_200_OK
    )
