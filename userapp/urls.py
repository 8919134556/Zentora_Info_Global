from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('user_home/', views.user_home, name='user_home'),
    path('api/gps-data/', views.gps_data_api, name='gps_data_api'),
    path("login/", views.user_login, name="user_login"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]