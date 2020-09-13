from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# def test_cors(request):
#     return render(request, 'test_cors.html')
#
#
# import json
#
#
# def test_cors_server(request):
#     # return HttpResponse('cross success')
#     json_str = json.dumps({'uname': 'tedu', 'age': 18})
#     return JsonResponse(json_str, safe=False)