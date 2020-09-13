from django.urls import path
from . import views

urlpatterns = [
    # # 127.0.0.1:8000/v1/users/sms
    path('sms',views.sms_view),
    # 127.0.0.1:8000/v1/users/tedu
    path('<str:username>',views.UsersView.as_view()),
    path('<str:username>/avatar',views.user_avatar),
]

