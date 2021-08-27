import re

from django.shortcuts import render

from index.models import User


def signin(request):
    if request.method == 'GET':
        return render(request, 'index/auth/signin.html')

    elif request.method == 'POST':
        number = request.POST.get('number')
        password = request.POST.get('password')

        return render(request, 'index/auth/signin.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'index/auth/signup.html')

    elif request.method == 'POST':
        number = request.POST.get('number')
        name = request.POST.get('name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = []

        if re.compile('^([0-9]){5}$').match(number) is None:
            errors.append('학번 형식이 잘못되었습니다.')
        elif User.objects.filter(number=number).count() > 0:
            errors.append('이미 존재하는 사용자입니다.')
        else:
            pass

        if len(name) < 2 or len(name) > 11:
            errors.append('이름 형식이 잘못되었습니다.')
        else:
            pass

        if re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d~!@#$%^&*()+|=]{8,20}$').match(password) is None:
            errors.append('비밀번호 형식이 잘못되었습니다.')
        else:
            pass

        if password != confirm_password:
            errors.append('비밀번호 확인이 일치하지 않습니다.')
        else:
            pass

        if len(errors) > 0:
            return render(request, 'index/auth/signup.html',
                          {'errors': errors, 'number': number, 'name': name, 'password': password,
                           'confirm_password': confirm_password})
        else:
            user = User.objects.create_user(number=number, name=name, password=password)
            user.save()

            return render(request, 'index/auth/signup-success.html')
