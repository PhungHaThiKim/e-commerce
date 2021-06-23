from django.db import transaction
from django.shortcuts import redirect, render
from user.models import User, Customer
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
from cart.models import Cart, CartItem
from product.models import Product, Item, Comment, Category
from order.models import Order, Payment, Shipment
from user.models import User, Address, Fullname
# Create your views here.

def index(request):
    return render(request, 'login.html')

def dologin(request):
    username = request.POST.dict()['username']
    password = request.POST.dict()['password']

    acc = User.objects.filter(username=username, password=password).first()
    if acc is not None:
        user_role = acc.role
        user_id = acc.id
        request.session['user_id'] = user_id
        if user_role == "Cus":
            return redirect('/product/')
        else:
            return redirect('/user/employee')
    else:
        return redirect('/user')

def logout(request):
    if "user_id" in request.session.keys():
        del request.session["user_id"]
    return redirect('/product')

def employee(request):
    return render(request, 'employee.html')

def regist(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        lastname = request.POST.get("lastname")
        fistname = request.POST.get("fistname")
        homenumber = request.POST.get("homenumber")
        street = request.POST.get("street")
        district = request.POST.get("district")
        city = request.POST.get("city")
        country = request.POST.get("country")
        sex = request.POST.get("sex")
        birthday = request.POST.get("birthday")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        print(username, password, lastname, fistname, homenumber, street, district, city, country, sex, birthday, phone,
              email)
        try:
            with transaction.atomic():
                user = User.objects.create(username=username, password=password, sex=sex, birthday="", phone=phone,
                                           email=email, role="Cus")
                fullname = Fullname.objects.create(userid=user, last=lastname, first=fistname)
                address = Address.objects.create(userid=user, homenum=homenumber, street=street, district=district,
                                                 city=city, country=country)
                cus = Customer.objects.create(type="Cus", userid=user)
            return redirect("/user")
            # messages.success(request, "Your item deleted from your cart.")
        except:
            print("insert faild")
            return redirect("/register")


    else:
        return render(request, 'register.html')
