from django.urls import path
from .views import *

urlpatterns = [
    path('leader-board', leader_board, name="leader-board"),
    path('previous-games', get_previous_games, name="previous-games"),
    path('add-point', add_point, name="add-point"),
]
