from django.urls import path

from .views import *

app_name = 'users'
urlpatterns = [
    path('register/', SignUpView.as_view(), name='sign_up'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
]