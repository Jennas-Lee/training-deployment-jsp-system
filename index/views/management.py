import re

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import auth

from index.models import User


def user_list(request):
    page_number = request.GET.get('page')

    model = User.objects.filter(is_active=1).order_by('number').all()
    request_count = User.objects.filter(is_active=0).order_by('number').count()
    paginator = Paginator(model, 15)
    page_obj = paginator.get_page(page_number)

    return render(request, 'index/management/user-list.html', {'page_obj': page_obj, 'request_count': request_count})


def request_list(request):
    page_number = request.GET.get('page')

    model = User.objects.filter(is_active=0).order_by('number').all()
    paginator = Paginator(model, 15)
    page_obj = paginator.get_page(page_number)

    return render(request, 'index/management/request-list.html', {'page_obj': page_obj})


def deny_list(request):
    page_number = request.GET.get('page')

    model = User.objects.filter(is_active=-1).order_by('number').all()
    paginator = Paginator(model, 15)
    page_obj = paginator.get_page(page_number)

    return render(request, 'index/management/deny-list.html', {'page_obj': page_obj})


def request_submit(request, user_number):
    user = User.objects.filter(number=user_number).last()
    error = ""

    if request.user.is_authenticated is False:
        error = "로그인이 필요합니다."
    elif request.user.is_admin is False:
        error = "관리자만 사용할 수 있는 기능입니다."
    elif user is None:
        error = "알 수 없는 사용자입니다."
    elif user.is_active == 1:
        error = "이미 승인된 사용자입니다."
    elif user.is_active == -1:
        error = "이미 승인을 거부한 사용자입니다."
    else:
        pass

    if error:
        return render(request, 'index/management/request-error.html', {'error': error})
    else:
        user.is_active = 1
        user.save()

        return redirect('user-list')


def request_deny(request, user_number):
    user = User.objects.filter(number=user_number).last()
    error = ""

    if request.user.is_authenticated is False:
        error = "로그인이 필요합니다."
    elif request.user.is_admin is False:
        error = "관리자만 사용할 수 있는 기능입니다."
    elif user is None:
        error = "알 수 없는 사용자입니다."
    elif user.is_active == 1:
        error = "이미 승인된 사용자입니다."
    else:
        pass

    if error:
        return render(request, 'index/management/request-error.html', {'error': error})
    else:
        user.is_active = -1
        user.save()

        return redirect('request-list')


def deny_submit(request, user_number):
    user = User.objects.filter(number=user_number).last()
    error = ""

    if request.user.is_authenticated is False:
        error = "로그인이 필요합니다."
    elif request.user.is_admin is False:
        error = "관리자만 사용할 수 있는 기능입니다."
    elif user is None:
        error = "알 수 없는 사용자입니다."
    elif user.is_active == 1:
        error = "이미 승인된 사용자입니다."
    else:
        pass

    if error:
        return render(request, 'index/management/request-error.html', {'error': error})
    else:
        user.is_active = 1
        user.save()

        return redirect('user-list')


def update_user(request, user_number):
    if request.method == 'GET':
        user = User.objects.filter(number=user_number).last()
        error = ""

        if request.user.is_authenticated is False:
            error = "로그인이 필요합니다."
        elif request.user.is_admin is False:
            error = "관리자만 사용할 수 있는 기능입니다."
        elif user is None:
            error = "알 수 없는 사용자입니다."
        elif user.is_active == 0:
            error = "승인하지 않은 사용자입니다."
        elif user.is_active == -1:
            error = "승인을 거부하거나 삭제한 사용자입니다."
        else:
            pass

        if error:
            return render(request, 'index/management/request-error.html', {'error': error})
        else:
            return render(request, 'index/management/update-user.html',
                          {'number': user.number, 'name': user.name, 'repository': user.repository,
                           'is_admin': user.is_admin})

    elif request.method == 'POST':
        number = request.POST.get('number')
        name = request.POST.get('name')
        repository = request.POST.get('repository')
        is_admin = request.POST.get('is_admin')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = []

        if user_number != number:
            if re.compile('^([0-9]){5}$').match(number) is None:
                errors.append('학번 형식이 잘못되었습니다.')
            elif User.objects.filter(number=number).count() > 0:
                errors.append('이미 존재하는 사용자입니다.')
            else:
                pass
        else:
            pass

        if len(name) < 2 or len(name) > 11:
            errors.append('이름 형식이 잘못되었습니다.')
        else:
            pass

        if password:
            if re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~!@#$%^&*()+|=]{8,20}$').match(password) is None:
                errors.append('비밀번호 형식이 잘못되었습니다.')
            else:
                pass

            if password != confirm_password:
                errors.append('비밀번호 확인이 일치하지 않습니다.')
            else:
                pass
        else:
            pass

        if len(errors) > 0:
            return render(request, 'index/management/update-user.html',
                          {'errors': errors, 'number': number, 'name': name, 'repository': repository,
                           'password': password, 'confirm_password': confirm_password, 'is_admin': is_admin})
        else:
            user = User.objects.filter(number=user_number).last()

            user.number = number
            user.name = name
            user.repository = repository
            user.is_admin = 1 if is_admin == "1" else 0

            if password:
                user.set_password(password)

            user.save()

            return redirect('user-list')


def delete_user(request, user_number):
    user = User.objects.filter(number=user_number).last()
    error = ""

    if request.user.is_authenticated is False:
        error = "로그인이 필요합니다."
    elif request.user.is_admin is False:
        error = "관리자만 사용할 수 있는 기능입니다."
    elif user is None:
        error = "알 수 없는 사용자입니다."
    elif user.is_active == -1:
        error = "이미 승인을 거부한 사용자입니다."
    elif user.is_active == 0:
        error = "승인을 하지 않은 사용자입니다."
    else:
        pass

    if error:
        return render(request, 'index/management/request-error.html', {'error': error})
    else:
        user.is_active = -1
        user.save()

        return redirect('user-list')
