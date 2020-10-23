import uuid
from django.db import models
from accounts.models import User
from django.conf import settings
import redis

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=2, decode_responses=True)

class CoinFlipGame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    GAME_STATES = (
        ('W', 'WAITING FOR PLAYER'),
        ('P', 'PLAYABLE'),
        ('E', 'ENDED'),
    )
    RESULT_CHOICES = (
        ('H', 'HEADS'),
        ('T', 'TAILS')
    )
    name = models.CharField(max_length=30)
    result = models.CharField(max_length=1, choices=RESULT_CHOICES, null=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="creator")
    opponent = models.ForeignKey(User, related_name='opponent', on_delete=models.PROTECT, null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="winner")
    bet = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "coinflip_games"

    @staticmethod
    def get_available_games():
        return CoinFlipGame.objects.filter(opponent=None)

    @staticmethod
    def created_count(user):
        return CoinFlipGame.objects.filter(creator=user)

    @staticmethod
    def get_games_for_player(user):
        from django.db.models import Q
        return CoinFlipGame.objects.filter(Q(opponent=user) |Q(creator=user))

    @staticmethod
    def get_by_id(id):
        try:
            return CoinFlipGame.objects.get(id=id)
        except CoinFlipGame.DoesNotExist:

            pass

    @staticmethod
    def create_new(user, name):
        new_game = CoinFlipGame(creator=user, name=name)


    @property
    def group_name(self):
        return "coinflip-%s" % self.id

