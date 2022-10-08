from django.urls import path
from .views import *


urlpatterns = [
    path('activate/<str:uid>/<str:token>',
         user_activate_account, name='user_activate_account'),
    path('activate/success', user_activate_account_succcess,
         name='user_activate_account_succcess'),
    path('password/reset/confirm/<str:uid>/<str:token>',
         reset_user_password, name='reset_user_password'),
    path('password/success', reset_password_success,
         name='reset_password_success')
]
