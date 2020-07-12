import redis
from rest_framework.decorators import api_view
from django.conf import settings

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)
redis_instance.set_response_callback('GET', int)  # GET VALUES AS INT

'''
@api_view(['GET'])
def leader_board(request):



@api_view(['GET'])
def get_previous_winners(requset):
'''