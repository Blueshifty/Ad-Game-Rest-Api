from rest_framework.response import Response
from rest_framework import status
from functools import wraps
import time


def print_execution_time(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        start_time = time.time()
        fn(*args, **kwargs)
        print(f'Executed {fn.__name__} in : {int(time.time() - start_time)} Seconds.')

    return inner


def login_api_required(required):
    def decorator(fn):
        @wraps(fn)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated == required:
                result = fn(request, *args, **kwargs)
                return result
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return wrapper

    return decorator
