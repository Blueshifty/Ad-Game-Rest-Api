from accounts.models import User
from datetime import datetime
from .models import Game
from .game_logic import create_game, start_lotto


def populate_database(people_count):
    for x in range(people_count):
        test_value = f'test_{x+100}'
        User.objects.create(
            user_name=test_value,
            email=f'{test_value}@testmail.com',
            password=test_value,
            date_of_birth=datetime.now(),
            profession='Tester',
            sex='M',
            phone_number='+905076559566',
            first_name=test_value,
            last_name=test_value
        )
