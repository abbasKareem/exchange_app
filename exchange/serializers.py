from .models import *
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'phone',  'first_name',
                  'last_name', 'password')


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['type_name']


class TranscationSerializer(serializers.ModelSerializer):
    tran_from = TypeSerializer()
    tran_to = TypeSerializer()

    class Meta:
        model = Transcation
        # depth = 1
        fields = ['tran_from', 'tran_to', 'amount']


class PaymentSerializer(serializers.ModelSerializer):

    transcation = TranscationSerializer()

    class Meta:
        model = Payment
        fields = ['create_at', 'hawala_number',
                  'status', 'recvied_amount', 'total', 'transcation']


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title', 'body']


class TranscationSerializer(serializers.ModelSerializer):
    tran_from = TypeSerializer()
    tran_to = TypeSerializer()

    class Meta:
        model = Transcation

        fields = ['tran_from', 'tran_to', 'amount']


class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'phone',  'first_name',
                  'last_name', 'start_date')
