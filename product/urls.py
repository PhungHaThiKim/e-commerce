from product import views
from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name = 'Home view' ),
    path('manageproduct', views.manageproduct, name="manageproduct"),
    path('deleteProduct/<int:id>', views.deleteProduct, name ='deleteProduct'),
    path('addProduct/', views.addProduct, name ='addProduct'),
    path('managecategory', views.managecategory, name="managecategory"),
    path('deleteCategory/<int:id>', views.deleteCategory, name='deleteCategory'),
    path('addCategory/', views.addCategory, name ='addCategory'),
    path('detail/<int:id>', views.productdetail, name = 'productdetail'),
    path('addcomment/', views.addcomment, name="addcomment"),
]