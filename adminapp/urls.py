from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('admin_home', views.admin_home, name='admin_home'),
    path('upload_vechile', views.upload_vechile, name='upload_vechile'),
    path('v_deatils', views.v_deatils, name='v_deatils'),
    path('popup/<int:id>', views.popup, name='popup'),
    path('fine', views.fine, name='fine'),
    path('fine_details', views.fine_details, name='fine_details'),
    path('fine_edit/<int:id>', views.fine_edit, name='fine_edit'),
    path('logout', views.logout, name='logout'),
]