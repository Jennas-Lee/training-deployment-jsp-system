from django.urls import path
from index.views.index.index import index
from index.views.auth.auth import signin, signup

index_urlpatterns = [
    path('', index, name='index'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup')
]
