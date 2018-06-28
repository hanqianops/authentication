import hashlib
import time

from rest_framework import exceptions
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers
from .utils.token_auth import TokenAuthenticate
from .utils.permission_auth import PermissionAuthenticate


class LoginView(APIView):
    """
    用于用户登录认证, 登陆成功后返回一个令牌
    """
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    def post(self,request,*args,**kwargs):

        ret = {'status':True,'msg':None}
        user = request.data.get('username')
        pwd = request.data.get('password')

        obj = models.User.objects.filter(username=user,password=pwd)
        if obj.exists():
            token = self.__md5(user)
            models.Token.objects.update_or_create(user=obj[0], defaults={'token': token})
            ret['token'] = token
            ret['msg'] = "认证成功"
        else:
            ret['status'] = False
            ret['msg'] = "用户名或密码错误"

        return Response(ret)

    def __md5(self,user):

        ctime = str(time.time())
        m = hashlib.md5(bytes(user, encoding='utf-8'))
        m.update(bytes(ctime, encoding='utf-8'))
        return m.hexdigest()




class PermissionView(APIView):
    """
    1、查看对象列表： GET /permission/
    2、查看对象: GET /permission/?id=1
    3、创建对象: POST /permission/   data = { "name": "更新组", "path": "/group/", "method": "PUT", "parameter": null }
    4、更新对象: PUT /permission/?id=1   data = { "name": "更新组", "path": "/group/", "method": "PUT", "parameter": null }
    5、删除对象: DELETE /permission/?id=1
    """
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # authentication_classes = [TokenAuthenticate, ]
    # permission_classes = [PermissionAuthenticate,]
    # def dispatch(self, request, *args, **kwargs):
    #     super

    def get_object(self, request):
        """获取指定对象"""
        pk = request.GET.get('id')

        try:
            return models.Permission.objects.get(pk=pk)
        except models.Permission.DoesNotExist:
            raise exceptions.AuthenticationFailed('必须指定一个对象id')

    def get(self, request, format=None):
        """获取对象列表 or 单个对象"""

        pk = request.GET.get("id")
        if pk:
            obj = models.Permission.objects.get(id=pk)
            serializer = serializers.PermissionSerializer(obj)
        else:
            obj = models.Permission.objects.all()
            serializer = serializers.PermissionSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """创建对象"""
        serializer = serializers.PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """更新对象"""
        obj = self.get_object(request)
        serializer = serializers.PermissionSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """删除对象"""
        obj = self.get_object(request)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupView(APIView):
    """
    1、查看对象列表： GET /group/
    2、查看对象: GET /group/?id=1
    3、创建对象: POST /group/   data = { "name": "运维组", "permission": [ { "name": "查看全部用户" } ] }
    4、更新对象: PUT /group/?id=1   data = { "name": "运维组", "permission": [ { "name": "查看全部用户" } ] }
    5、删除对象: DELETE /group/?id=1

    """
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    # authentication_classes = [TokenAuthenticate, ]
    # permission_classes = [PermissionAuthenticate,]


    def get_object(self, request):
        """获取指定对象"""
        pk = request.GET.get('id')
        try:
            return models.Group.objects.get(pk=pk)
        except models.Group.DoesNotExist:
            raise exceptions.AuthenticationFailed('必须指定一个对象id')

    def get(self, request, format=None):
        """获取对象列表 or 单个对象"""

        pk = request.GET.get("id")
        if pk:
            obj = models.Group.objects.get(id=pk)
            serializer = serializers.GroupSerializer(obj)
        else:
            obj = models.Group.objects.all()
            serializer = serializers.GroupSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """创建对象"""
        serializer = serializers.GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """更新对象"""
        obj = self.get_object(request)
        serializer = serializers.GroupSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """删除对象"""
        obj = self.get_object(request)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserView(APIView):
    """
    1、查看对象列表： GET /user/
    2、查看对象: GET /user/?id=1
    3、创建对象: POST /user/   data = {"username": "han", "password": "123", "group": [{"name": "开发组"}]}
    4、更新对象: PUT /user/?id=1   data = {"username": "han", "password": "123", "group": [{"name": "开发组"}]}
    5、删除对象: DELETE /user/?id=1
    """

    parser_classes = [JSONParser, FormParser, MultiPartParser]
    permission_classes = [PermissionAuthenticate,]
    authentication_classes = [TokenAuthenticate,]

    def get_object(self, request):
        """获取指定对象"""
        pk = request.GET.get('id')
        try:
            return models.User.objects.get(pk=pk)
        except models.TUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('必须指定一个对象id')

    def get(self, request, format=None):
        """获取对象列表 or 单个对象"""
        print(request.user,request.auth)
        pk = request.GET.get("id")
        if pk:
            obj = models.User.objects.get(id=pk)
            serializer = serializers.UserSerializer(obj)
        else:
            obj = models.User.objects.all()
            serializer = serializers.UserSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """创建对象"""
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        """更新对象"""
        obj = self.get_object(request)
        serializer = serializers.UserSerializer(obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        """删除对象"""
        obj = self.get_object(request)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


