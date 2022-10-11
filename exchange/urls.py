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
         name='reset_password_success'),

    path('api/payment', CreatePaymentView.as_view()),
    path('api/my_payment', ListMyPaymentsView.as_view()),
    path('api/my_notify', ListAllNotificationsView.as_view()),
    path('api/all_transcations', AllTranscationsView().as_view()),
    path('api/all_typs', AllTypeView().as_view()),


]
