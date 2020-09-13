from django.db import models
import random

def default_sign():
    signs = ['风里雨里香格里拉等你','风里雨里419等你']
    return random.choice(signs)

# Create your models here.

class UserProfile(models.Model):
    username = models.CharField("用户名", max_length=11, primary_key=True)
    nickname = models.CharField("昵称", max_length=50)
    email = models.EmailField("邮箱")
    password = models.CharField("密码", max_length=32)
    sign = models.CharField("个人签名", max_length=50, default=default_sign)
    info = models.CharField("个人描述", max_length=150, default='')
    avatar = models.ImageField("头像", upload_to='avatar', null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("修改时间", auto_now=True)
    phone = models.CharField("手机", max_length=11, default='')
    birthday = models.CharField("生日", max_length=10, default='')

    class Meta:
        db_table = 'user_table'