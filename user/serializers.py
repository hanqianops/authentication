from rest_framework import serializers
from . import models
from rest_framework import exceptions
from rest_framework.compat import set_many


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Permission
        fields = '__all__'
        depth = 2

class GroupSerializer(serializers.ModelSerializer):

    permission = PermissionSerializer(many=True)
    class Meta:
        model = models.Group
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        group = [ i['name'] for i in validated_data.pop('permission')]
        group_obj = models.Permission.objects.filter(name__in=group)
        new_user = models.Group.objects.create(**validated_data)
        new_user.permission = list(group_obj)
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
        group = [i['name'] for i in validated_data.pop('permission')]
        group_obj = models.Permission.objects.filter(name__in=group)
        instance.permission = list(group_obj)
        for key in instance._meta.fields:
            if key.name in validated_data:
                setattr(instance, key.name, validated_data[key.name])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    group = GroupSerializer(many=True)
    class Meta:
        model = models.User
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        group = [ i['name'] for i in validated_data.pop('group')]
        group_obj = models.Group.objects.filter(name__in=group)
        new_user = models.User.objects.create(**validated_data)
        new_user.group = list(group_obj)
        new_user.save()
        return new_user

    def update(self, instance, validated_data):
        group = [i['name'] for i in validated_data.pop('group')]
        group_obj = models.Group.objects.filter(name__in=group)
        instance.group = list(group_obj)
        for key in instance._meta.fields:
            if key.name in validated_data:
                setattr(instance, key.name, validated_data[key.name])
        instance.save()
        return instance