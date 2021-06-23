from datetime import datetime

from django.shortcuts import render, redirect

from feedback.models import Feedback
from user.models import User
from order.models import Payment,Shipment, Order
from django.db import transaction
from cart.models import CartItem,Cart
from product.models import Item, Product, Supplier, Category, Comment
from user.models import User, Customer, Fullname, Address
# Create your views here.

def index(request):
    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)
    cus = Customer.objects.get(userid=user)
    orders = Order.objects.filter(customeruserid=cus)
    cartitem = None
    if request.POST.get("process", "") == "feedback":
        content = request.POST.get("content", "")
        rate = request.POST.get("rate", "")
        cartitemid = request.POST.get("cartitemid", "")
        cartitemp = CartItem.objects.get(id=cartitemid)
        try:
            with transaction.atomic():
                Feedback.objects.create(
                    content=content,
                    star=rate,
                    time=datetime.now().strftime("%Y-%m-%d"),
                    status="Success",
                    cartitemid=cartitemp,
                    customeruserid=cus
                )
            return redirect("/order")
        except Exception as e:
            print(e)
            print("delete faild")
    else:
        cartitemid = request.GET.get("feedback", "")

        if cartitemid != "":
            cartitem = CartItem.objects.get(id=cartitemid)

    return render(request, 'orders.html', {'orders': orders, 'cartitem': cartitem})

def manageshipment(request):

    addmodel = request.GET.get('add')
    if "user_id" in request.session.keys():
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        payment = Payment.objects.all()
        shipment = Shipment.objects.all()
        print("user_id", user)

    else:
        user = None
    return render(request,'manageshipment.html', {'payment': payment,
                                                 'user': user, 'shipment': shipment, 'addmodel': addmodel})
def deleteShip(request, id):
    try:
        with transaction.atomic():
            Shipment.objects.filter(id=id).delete()

    except Exception as e:
        print(e)
        print("delete faild")

    return redirect("/order/manageshipment")

def addShipment(request):
    if request.method == "POST":
        shipment_type = request.POST.get("shipment_type")
        shipment_price = request.POST.get("shipment_price")

        print(shipment_type, shipment_price)
        try:
            with transaction.atomic():
                shipment = Shipment.objects.create(type=shipment_type,
                                       price=shipment_price,
                                       )
                print(shipment)

        except Exception as e:

            print(e)
            print("insert faild")

        return redirect("/order/manageshipment")
    else:
        return redirect("/order/manageshipment")

# view payment
def managepayment(request):

    addmodel = request.GET.get('add')
    if "user_id" in request.session.keys():
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        payment = Payment.objects.all()
        shipment = Shipment.objects.all()
        print("user_id", user)

    else:
        user = None
    return render(request,'managepayment.html', {'payment': payment,
                                                 'user': user, 'shipment': shipment, 'addmodel': addmodel})
def deletePay(request, id):
    try:
        with transaction.atomic():
            Payment.objects.filter(id=id).delete()

    except Exception as e:
        print(e)
        print("delete faild")

    return redirect("/order/managepayment")

def addPayment(request):
    if request.method == "POST":
        payment_type = request.POST.get("payment_type")
        payment_discountrate = request.POST.get("payment_discountrate")

        print(payment_type, payment_discountrate)
        try:
            with transaction.atomic():
                payment = Payment.objects.create(type=payment_type,
                                       discountrate=payment_discountrate,
                                       )
                print(payment)

        except Exception as e:

            print(e)
            print("insert faild")

        return redirect("/order/managepayment")
    else:
        return redirect("/order/managepayment")

def manageorder(request): # get toan bo order
    orders = []
    for o in Order.objects.all():
        orders.append(o)
    orderid = request.GET.get('orderid')
    print(orderid)
    order = None
    if orderid is not None:
        order = Order.objects.get(id = orderid)
        # print(order.userid.fullname_set.all()[0].first)

    return render(request, 'manageorder.html', {'orders': orders, 'order': order})

def goorderdetail(request, id): # get order detail
    orderdetail = Order.objects.get(ID=id)
    cart = Cart.objects.get(ID=order.cartID)
    cartitems = []
    print(orderdetail)
    items = []
    for ci in CartItem.objects.filter(CartID=cart.ID):
        cartitems.append(ci)
        for i in Item.objects.filter(ID=ci.ItemID):
            items.append(i)
    return render(request, 'manageorder.html', { 'orderdetail': orderdetail})

def setorderchecked(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid')
        print('Orderid', orderid)
        Order.objects.filter(id=orderid).update(state='Confirmed')
        return redirect('/order/manageorder')
    else:
        return redirect('/order/manageorder')


def setordercancel(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid')
        print('Orderid', orderid)
        Order.objects.filter(id=orderid).update(state='Canceled')
        return redirect('/order/manageorder')
    else:
        return redirect('/order/manageorder')


def checkout(request):

    payments = Payment.objects.all()
    shipments = Shipment.objects.all()

    return render(request, 'checkout.html', {'payments': payments, 'shipments': shipments})

def confirm(request):

    homenumber = request.GET.get("homenumber")
    street = request.GET.get("street")
    district = request.GET.get("district")
    city = request.GET.get("city")
    country = request.GET.get("country")
    fullname = request.GET.get("fullname")
    phone = request.GET.get("phone")
    shipmentid = request.GET.get("shipment")
    paymentid = request.GET.get("payment")
    shipment = Shipment.objects.get(id=shipmentid)
    payment = Payment.objects.get(id=paymentid)

    user_id = request.session['user_id']
    print('user_id', user_id)
    user = User.objects.get(id=user_id)
    if request.POST.get("proceed") == "confirm":
        cartid = request.POST.get("cartid")
        cart = Cart.objects.get(id=cartid)
    else:
        cart = Cart.objects.filter(state=0, userid=user).first()
    total = 0
    if cart is not None:
        cartitems = CartItem.objects.filter(cartid=cart)
        for cartitem in cartitems:
            total += cartitem.cost * cartitem.quantity
    else:
        cartitems = None

    fulltoal = (total+shipment.price)*(1-payment.discountrate)
    order = None
    if request.POST.get("proceed") == "confirm":
        order = Order.objects.filter(customeruserid=user_id, cartid=cart).first()
        if order is None:
            try:
                with transaction.atomic():
                    cus = Customer.objects.get(userid=user_id)
                    order = Order.objects.create(
                        customeruserid=cus,
                        cartid=cart,
                        paymentid=payment,
                        shipmentid=shipment,
                        num=fulltoal,
                        time=datetime.now().strftime("%Y-%m-%d"),
                        state="Pending",
                        address="{} {}, {}, {}, {}".format(homenumber, street, district, city, country)
                    )
                    cart = Cart.objects.filter(id=cart.id).update(state=1)
            except Exception as e:
                print(e)
                print("insert faild")


    print("order", order)

    return render(request, 'confirmview.html', {
        'homenumber': homenumber,
        'street': street,
        'district': district,
        'city': city,
        'country': country,
        'shipment': shipment,
        'payment': payment,
        'cartitems': cartitems,
        'cart': cart,
        'total': total,
        'user': user,
        'phone': phone,
        'fullname': fullname,
        'order': order
    })
