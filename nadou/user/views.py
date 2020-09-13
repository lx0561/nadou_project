from django.shortcuts import render

# Create your views here.
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

import json
from user.models import UserProfile
import hashlib
from btoken.views import make_token
import time
import jwt
from tools.logging_dec import logging_check
from django.utils.decorators import method_decorator
from django.core.cache import cache
from tools.sms import YunTongXin
from django.conf import settings
from .tasks import send_sms

# Create your views here.

# user的code: 10100~10199
class UsersView(View):
    def get(self, request,username=None):
        if username:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                print("get user error %s"% e)
                result={'code':10104,'error':'username is wrong'}
                return JsonResponse(result)
            # 根据查询字符串的键获取指定的属性
            if request.GET.keys():
                data={}
                for k in request.GET.keys():
                    if k == 'password':
                        continue  # 过滤敏感信息
                    if hasattr(user,k): # 判断有这个键
                        data[k] = getattr(user,k) # 把对应的键的值加到字典
                result = {'code':200,'username':username,'data':data}
                return JsonResponse(result)
            else:
                result={'code':200,'username':username,
                        'data':{'info':user.info,'sign':user.sign,
                                'nickname':user.nickname,'avatar':str(user.avatar)}}
                return JsonResponse(result)
        else:
            return HttpResponse("--all users--")

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        email = json_obj['email']
        phone = json_obj['phone']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        sms_num = json_obj['sms_num']
        # 校验验证码
        cache_key = 'sms_%s' % phone
        old_code = cache.get(cache_key)
        # 验证码过期
        if not old_code:
            result = {'code':10113,'error':'code is wrong'}
            return JsonResponse(result)
        # 比较
        if int(sms_num) != old_code:
            result = {'code': 10114, 'error': 'code is wrong2'}
            return JsonResponse(result)

        if len(username) > 11:
            result = {'code': 10100, 'error': 'username is too long'}
            return JsonResponse(result)
        # 用户名是否可用
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10101, 'error': 'username is exist'}
            return JsonResponse(result)
        # 处理密码
        if password_1 != password_2:
            result = {'code': 10102, 'error': 'password is error'}
            return JsonResponse(result)
        md5 = hashlib.md5()
        md5.update(password_1.encode())
        password_m = md5.hexdigest()
        # 插入数据
        try:
            user = UserProfile.objects.create(username=username,
                                              password=password_m, email=email,
                                              phone=phone, nickname=username)
        except Exception as e:
            print('create error is %s' % e)
            result = {'code': 10101, 'error': 'username is exist'}
            return JsonResponse(result)

        # 签发jwt
        token = make_token(username)
        return JsonResponse({'code': 200,'username':username,'data':{'token':token.decode()}})

    # 更新个人信息
    @method_decorator(logging_check)
    def put(self,request,username):
        # 不使用第三个参数了,user从装饰器中给request增加的附加属性myuser获取
        json_str = request.body
        json_obj = json.loads(json_str)
        request.myuser.sign = json_obj["sign"]
        request.myuser.nickname = json_obj["nickname"]
        request.myuser.info = json_obj["info"]
        request.myuser.save()
        result = {'code':200,'username':request.myuser.username}
        return JsonResponse(result)

@logging_check
def user_avatar(request,username):
    if request.method != 'POST':
        result = {'code':10105,'erorr':'please give me POST'}
        return JsonResponse(result)
    # 1.从url中获取username
    # user = UserProfile.objects.get(username=username)

    # 2.从装饰器中由requset的附加属性myuser获取user
    user = request.myuser
    user.avatar = request.FILES['avatar']
    user.save()
    # result={'code':200,'username':username}
    result={'code':200,'username':username}
    return JsonResponse(result)

def sms_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    phone =json_obj['phone']
    print(phone)
    # 防止用户多次点击按钮重复发送验证码
    cache_key = 'sms_%s' % (phone)
    old_code = cache.get(cache_key)
    if old_code:
        result={'code':10112,'error':'请稍后再来'}
        return JsonResponse(result)
    # 生成随机码
    code = random.randint(1000,9999)
    print(code)
    # 放到缓存中
    cache.set(cache_key,code,65)
    # 同步发送
    # x = YunTongXin(settings.SMS_ACCOUNT_ID, settings.SMS_ACCOUNT_TOKEN,
    #                settings.SMS_APP_ID, settings.SMS_TEMPLATE_ID)
    # res = x.run('13388175276', code)
    # print(res)
    # 异步发送
    send_sms.delay(phone, code)

    return JsonResponse({'code':200})

