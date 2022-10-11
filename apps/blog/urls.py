from django.urls import path

from .views import *


app_name = 'blog'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blog/', BlogView.as_view(), name='index'),
    path('blog/<slug>/', post_detail, name='detail'),
    path('like/<slug>/', like, name='like'),
]