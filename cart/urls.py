from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('addtocartget', views.addtocartget, name="addtocart"),
    path('deletecartget', views.deletecartget, name="deletecartget"),
    path('docartitem', views.docartitem, name="docartitem")
]