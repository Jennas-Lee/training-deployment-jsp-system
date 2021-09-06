from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import auth

from index.models import User


def status(request):
    return render(request, 'index/application/status.html', {})


def register(request):
    return render(request, 'index/dashboard/status.html', {})
