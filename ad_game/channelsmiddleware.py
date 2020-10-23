from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from accounts.models import User
from urllib.parse import parse_qs
from django.conf import settings
from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser


@database_sync_to_async
def get_user(token):
    try:
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        # print(e)
        return None
    else:
        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.get(id=decoded_data["user_id"])
        except User.DoesNotExist:
            return AnonymousUser()
        return user

class JwtTokenAuthMiddleWareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        self.scope['user'] = await get_user(parse_qs(self.scope["query_string"].decode("utf8"))["token"][0])
        inner = self.inner(self.scope)
        return await inner(receive, send)


class JwtTokenAuthMiddleWare:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JwtTokenAuthMiddleWareInstance(scope, self)


JwtTokenAuthMiddleWareStack = lambda inner: JwtTokenAuthMiddleWare(AuthMiddlewareStack(inner))
