from django.shortcuts import render


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
