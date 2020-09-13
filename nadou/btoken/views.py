from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json
from user.models import UserProfile
import hashlib
import time
import jwt
from django.conf import settings

# error code :10200~10299
# Create your views here.
class TokenView(View):
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        password = json_obj['password']
        try:
            old_user = UserProfile.objects.get(username=username)
        except Exception as e:
            print('error is %s' % e)
            result = {'code':10201,'error':'uname or password error'}
            return JsonResponse(result)
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_m = md5.hexdigest()
        if password_m != old_user.password:
            result = {'code': 10201, 'error': 'uname or password error'}
            return JsonResponse(result)
        # 签发token
        token = make_token(username)
        return JsonResponse({'code': 200,'username':username,'data':{'token':token.decode()}})

    def get(self, request):
        return HttpResponse('-token get-')

def make_token(username, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'username': username, 'exp': now + expire}
    return jwt.encode(payload,key,algorithm='HS256')