from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import authentication
from rest_framework import pagination

from .models import *
from .serializers import *
from .utils import my_response
from datetime import datetime


# datetime object containing current date and time

class CreatePaymentView(generics.CreateAPIView):

    def post(self, request):
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d%m%Y%H%M%S")

        tran_from = request.data['from']
        user_player_id = request.data['user_player_id']
        tran_to = request.data['to']
        recvied_amount = request.data['recvied_amount']

        try:
            type_from_obj = Type.objects.get(type_name=tran_from)
        except Type.DoesNotExist:
            return my_response(False, 'transaction type from not found', {}, status.HTTP_404_NOT_FOUND)
        try:
            type_to_obj = Type.objects.get(type_name=tran_to)
        except Type.DoesNotExist:
            return my_response(False, 'transaction type to not found', {}, status.HTTP_404_NOT_FOUND)

        # user_first_name = request.user.first_name
        # user = CustomUser.objects.get(first_name=user_first_name)

        transcation_obj = Transcation.objects.get(
            tran_from=type_from_obj.pk, tran_to=type_to_obj.pk)

        total = transcation_obj.amount + recvied_amount

        hawala_number = dt_string

        mac_in_str = f"{request.user.pk}{transcation_obj.tran_from}{recvied_amount}{transcation_obj.tran_to}"
        result = hashlib.md5(mac_in_str.encode())
        result_final = result.hexdigest()

        payment_obj = Payment.objects.create(
            user=request.user, transcation=transcation_obj, total=total, recvied_amount=recvied_amount, hawala_number=hawala_number, status='Pending', mac_in=result_final)
        payment_obj.save()

        notify = Notification.objects.create(
            user=request.user, title="انشاء دفع", body="تم عملية التحويل بنجاح، يرجى الانتظار لحين موافق الادمن على عملية التحويل")

        try:
            signal_obj = OneSignal.objects.get(user=request.user)
        except OneSignal.DoesNotExist:
            one_signal_obj = OneSignal.objects.create(
                user=request.user, user_notify_id=user_player_id)
            one_signal_obj.save()
        OneSignal.objects.filter(user=request.user).update(
            user_notify_id=user_player_id)

        data = {
            "payment_id": payment_obj.pk,
            "create_at": payment_obj.create_at,
            "status": payment_obj.status[0],
            "hawala_number": payment_obj.hawala_number,
            "total": payment_obj.total,
            "recvied_amount": payment_obj.recvied_amount,
            "status": payment_obj.status
        }
        return my_response(True, 'Payment Created Successfully!', data, status.HTTP_201_CREATED)


class ListMyPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return Payment.objects.filter(user=self.request.user).order_by('-id')

    def list(self, request):
        all_payment_obj = Payment.objects.filter(
            user=request.user).order_by('-id')
        if not all_payment_obj:
            return my_response(True, "You don't have any payment yet", {}, status.HTTP_200_OK)
        serializer = PaymentSerializer(all_payment_obj, many=True)

        return my_response(True, 'All payment done', serializer.data, status.HTTP_200_OK)


class ListAllNotificationsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        all_notifications = Notification.objects.filter(
            user=request.user).order_by('-id')[:20]
        if not all_notifications:
            return my_response(True, "You don't have any notifications yet", {}, status.HTTP_200_OK)
        serializer = NotificationsSerializer(all_notifications, many=True)

        return my_response(True, 'notifications fetched successfully', serializer.data, status.HTTP_200_OK)


class AllTranscationsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        qs = Transcation.objects.all().order_by('-id')
        serializer = TranscationSerializer(qs, many=True)
        return my_response(True, 'Transcations fetched successfully', serializer.data, status.HTTP_200_OK)


class AllTypeView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        qs = Type.objects.all().order_by('-id')
        serializer = TypeSerializer(qs, many=True)
        return my_response(True, 'Typs fetched successfully', serializer.data, status.HTTP_200_OK)


# ====================================================


def user_activate_account(request, uid, token):
    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'user_activate_account.html', context=context)


def user_activate_account_succcess(request):
    return render(request, 'user_activate_account_succcess.html')


def reset_user_password(request, uid, token):

    context = {
        'uid': uid,
        'token': token
    }
    return render(request, 'reset_user_password.html', context=context)


def reset_password_success(request):
    return render(request, 'password_done.html')
