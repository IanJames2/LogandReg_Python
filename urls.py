from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('users', views.register),
    path('addmovie', views.movie_input),
    path('movie_added', views.added_movie),
    path('logout', views.logout)
]

#dashboard = success