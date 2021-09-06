import docker

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import auth

from index.models import User


def dashboard(request):
    page_number = request.GET.get('page')
    models = []
    users = User.objects.order_by('number').all()
    # client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    for user in users:
        # container_status = None
        # try:
        #     container_status = client.containers.get(user.number)
        # except docker.errors.NotFound:
        #     container_status = None

        model = {
            'number': user.number,
            'name': user.name,
            'repository': user.repository,
            # 'container_status': container_status
            'container_status': 1
        }
        models.append(model)

    paginator = Paginator(models, 15)
    page_obj = paginator.get_page(page_number)

    #
    # client.containers.list(all=True, filters={'network': 'jspnet'})
    #
    # client.close()

    return render(request, 'index/dashboard/status.html', {'page_obj': page_obj})
