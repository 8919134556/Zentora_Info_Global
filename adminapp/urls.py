from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path('admin_login', views.admin_login_page, name='admin_login'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('upload_vechile', views.upload_vechile, name='upload_vechile'),
    path('v_details', views.v_details, name='v_details'),
    path("approve-user/<int:user_id>/", views.approve_user, name="approve_user"),
    path("reject-user/<int:user_id>/", views.reject_user, name="reject_user"),
    path('popup/<int:id>', views.popup, name='popup'),

    
    path('add_emp', views.add_emp, name='add_emp'),
    path('fine', views.fine, name='fine'),
    path('fine_edit/<int:id>', views.fine_edit, name='fine_edit'),
    path('logout', views.logout, name='logout'),
]