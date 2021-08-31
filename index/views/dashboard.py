import docker

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import auth

from index.models import User


def dashboard(request):
    client = docker.DockerClient(base_url='tcp://hub.docker.internal')
    return render(request, 'index/dashboard/status.html')
