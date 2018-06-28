import time

from django.conf import settings
from rest_framework import exceptions

from .. import models


class TokenAuthenticate(object):
    """验证令牌是否正确，并验证令牌是否在有效期内"""
    def authenticate(self, request):
        token = request.META.get('HTTP_TOKEN')
        token_obj = models.Token.objects.filter(token=token)
        if token_obj.exists():
            expire_time = time.mktime(token_obj[0].update_time.timetuple()) + settings.TOKEN_EXPIRE
            current_time = time.time()
            if expire_time < current_time:
                raise exceptions.AuthenticationFailed('令牌已经过期')
            return (token_obj[0].user.username, True)  # request.user = 'xxx' request.auth = True
        else:
            raise exceptions.AuthenticationFailed('令牌验证错误')

    def authenticate_header(self, val):
        pass