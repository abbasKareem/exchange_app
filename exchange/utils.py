from rest_framework.response import Response


def my_response(success, message, data, status_code):
    return Response({
        'success': success,
        'message': message,
        'data': data
    }, status=status_code)
