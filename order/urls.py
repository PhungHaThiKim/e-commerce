from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('manageshipment', views.manageshipment, name="manageshipment"),
    path('deleteShipment/<int:id>', views.deleteShip, name ='deleteShipment'),
    path('addShipment/', views.addShipment, name ='addShipment'),
    path('managepayment', views.managepayment, name="managepayment"),
    path('deletePayment/<int:id>', views.deletePay, name ='deletePayment'),
    path('addPayment/', views.addPayment, name='addPayment'),
    path('manageorder', views.manageorder, name="manageorder"),
    path('manageorder/orderchecked', views.setorderchecked, name='setorderchecked'),
    path('manageorder/ordercanceled', views.setordercancel, name='setordercancel'),
    path('checkout', views.checkout, name="checkout"),
    path('confirm', views.confirm, name="confirm")
]