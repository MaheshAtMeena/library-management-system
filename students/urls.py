from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register, name='register'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('mark/<uuid:token>/', views.mark_attendance_token, name='mark_attendance_token'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

]
