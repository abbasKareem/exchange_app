import requests
from rest_framework.response import Response


def my_response(success, message, data, status_code):
    return Response({
        'success': success,
        'message': message,
        'data': data
    }, status=status_code)


def send_notifiy(player_id, message):
    url = "https://onesignal.com/api/v1/notifications"

    payload = {
        "app_id": "316ae9f8-0793-44e5-8eaf-27ce6abc6438",
        "include_player_ids": [player_id],
        "data": {"foo": "bar"},
        "contents": {"en": message}
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Basic NTE5ZDllY2MtZWIyMy00YzA1LTlkZmUtN2RjMjdiMDE2MDkw",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.status_code
