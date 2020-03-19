from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user', views.user, name='user'),
    path('topsongs', views.topsongs, name='topsongs'),
    path('help', views.help, name='help'),
    path('trending', views.trending, name='trending'),
    path('myreviews', views.user_reviews, name='myreviews'),
    path('friends', views.friends, name='friends'),
    path('usersongs', views.user_songs, name='mysongs'),
    path('review', views.review, name='review'),
    path('editreview', views.edit_review, name='editreview'),
    path('upvote', views.upvote, name='upvote'),
    path('downvote', views.downvote, name='downvote')
]
