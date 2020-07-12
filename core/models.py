from django.db import models
from accounts.models import User


class Game(models.Model):
    STATE_CHOICES = (
        ('S', 'STARTED'),
        ('E', 'ENDED'),
        ('P', 'PAID')
    )

    winner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    total_point = models.IntegerField(null=True, blank=True)
    prize = models.IntegerField(null=True, blank=True)
    game_state = models.CharField(max_length=1, choices=STATE_CHOICES)
