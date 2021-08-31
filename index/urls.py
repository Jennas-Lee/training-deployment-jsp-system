from django.urls import path
from index.views.index import index
from index.views.auth import signin, signup, signout, mypage
from index.views.management import user_list, request_list, deny_list, request_submit, request_deny, deny_submit, \
    update_user, delete_user
from index.views.dashboard import dashboard

index_urlpatterns = [
    path('', index, name='index'),
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('mypage/', mypage, name='mypage'),

    path('admin/list/', user_list, name='user-list'),
    path('admin/list/request', request_list, name='request-list'),
    path('admin/list/deny', deny_list, name='deny-list'),
    path('admin/request/submit/<str:user_number>', request_submit, name='request-submit'),
    path('admin/request/deny/<str:user_number>', request_deny, name='request-deny'),
    path('admin/deny/submit/<str:user_number>', deny_submit, name='deny-submit'),
    path('admin/update/<str:user_number>', update_user, name='update-user'),
    path('admin/delete/<str:user_number>', delete_user, name='delete-user'),

    path('dashboard/status', dashboard, name='dashboard'),
]
