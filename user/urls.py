from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('dologin', views.dologin, name="dologin"),
    path('logout', views.logout, name="logout"),
    path('regist', views.regist, name="regist"),
    path('employee', views.employee, name="employee")

]