from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user', views.user, name='user'),
    path('topsongs', views.topsongs, name='topsongs'),
    path('help', views.help, name='help'),
    path('trending', views.trending, name='trending')
]
