import time

from rest_framework import exceptions

from .. import models
from rest_framework import permissions

class PermissionAuthenticate(permissions.BasePermission):
    """验证用户权限"""
    def has_permission(self, request, view):
        if self.admin_permission(request):
            return True

        if self.url_permission(request):
            return True

        raise exceptions.AuthenticationFailed('没有权限执行此操作')


    def url_permission(self,request):
        obj = models.User.objects.filter(username=request.user,
                                                  group__permission__path=request.path,
                                                  group__permission__method=request.method).exists()
        if obj:
            return True

    def admin_permission(self,request):
        obj = models.User.objects.filter(username=request.user, group__name='管理组')
        if obj.exists():
            return True
