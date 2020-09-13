# Generated by Django 2.2.12 on 2020-09-09 21:05

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('username', models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='用户名')),
                ('nickname', models.CharField(max_length=50, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('sign', models.CharField(default=user.models.default_sign, max_length=50, verbose_name='个人签名')),
                ('info', models.CharField(default='', max_length=150, verbose_name='个人描述')),
                ('avatar', models.ImageField(null=True, upload_to='avatar', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('phone', models.CharField(default='', max_length=11, verbose_name='手机')),
                ('birthday', models.CharField(default='', max_length=10, verbose_name='生日')),
            ],
            options={
                'db_table': 'user_table',
            },
        ),
    ]