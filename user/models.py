from django.db import models


class Group(models.Model):
    """用户组"""
    name = models.CharField(verbose_name="组名",max_length=255, unique=True)
    permission = models.ManyToManyField(verbose_name="可访问路径", to="Permission")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 't_group'


class User(models.Model):
    """用户表"""
    username = models.CharField(verbose_name="用户名",max_length=255, unique=True)
    password = models.CharField(verbose_name="密码",max_length=255, blank=True, null=True)
    group = models.ManyToManyField(verbose_name="组名", to='Group',)
    #permission = models.ManyToManyField(verbose_name="可访问路径", to='TPermission')

    def __str__(self):
        return self.username
    class Meta:
        db_table = 't_user'

class Permission(models.Model):
    """权限表"""
    name = models.CharField(verbose_name="权限名称",max_length=255, blank=True, null=True)
    path = models.CharField(verbose_name="访问路径",max_length=255, blank=True, null=True)
    method_choices = (('GET','GET'), ('POST','POST'), ('PUT','PUT'),('DELETE','DELETE'),)
    method = models.CharField(verbose_name="请求方法",choices=method_choices,max_length=16, blank=True, null=True)
    parameter = models.CharField(verbose_name="请求参数",max_length=255, blank=True, null=True)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.name,self.method,self.path)
    class Meta:
        db_table = 't_permission'


class Token(models.Model):
    user = models.ForeignKey(verbose_name="用户", to="User")
    token = models.CharField(verbose_name="令牌",max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    class Meta:
        db_table = 't_token'