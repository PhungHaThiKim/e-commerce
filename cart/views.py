from django.db import transaction
from django.shortcuts import render, redirect


# Create your views here.
from cart.models import Cart, CartItem
from product.models import Item
from user.models import User

def index(request):
    user_id = request.session['user_id']
    print('user_id', user_id)
    user = User.objects.get(id=user_id)
    cart = Cart.objects.filter(state=0, userid=user).first()
    total = 0
    if cart is not None:
        cartitems = CartItem.objects.filter(cartid=cart)
        for cartitem in cartitems:
            total += cartitem.cost*cartitem.quantity
    else:
        cartitems = None


    return render(request, 'cart.html', {'cartitems': cartitems, 'total': total})


def addtocartget(request):
    user_id = request.session['user_id']
    print('user_id', user_id)
    user = User.objects.get(id=user_id)
    item_id = request.GET.get('item', '')
    print('item_id', item_id)
    item = Item.objects.get(id=item_id)
    try:
        with transaction.atomic():
            cart = Cart.objects.filter(state=0, userid=user).first()
            if cart is None:
                print("Create new cart")
                cart = Cart.objects.create(state=0, userid=user)
            print("cartid:", cart.id)
            cartitem = CartItem.objects.filter(itemid=item, cartid=cart).first()
            if cartitem is None:
                cartitem = CartItem.objects.create(quantity=1, cost=item.outprice, cartid=cart, itemid=item)
            else:
                CartItem.objects.filter(itemid=item, cartid=cart).update(quantity=cartitem.quantity+1, cost=item.outprice)

            print("cartitemid:", cartitem.id)

    except Exception as e:
        print(e)
        print("add to cart faild")

    if request.GET.get("before", "") != "":
        return redirect('/product/detail/'+request.GET.get("before", ""))

    return redirect('/product')

def deletecartget(request):
    cartitem_id = request.GET.get('cartitem', '')
    print('cartitem_id', cartitem_id)
    try:
        with transaction.atomic():
            CartItem.objects.filter(id=cartitem_id).delete()

    except Exception as e:
        print(e)
        print("deletecartget faild")

    return redirect('/cart')

def docartitem(request):

    if request.POST.get("proceed") == "Detail":

        user_id = request.session['user_id']
        print('user_id', user_id)
        user = User.objects.get(id=user_id)
        item_id = request.POST.get('item', '')
        print('item_id', item_id)
        item = Item.objects.get(id=item_id)

        quanti = request.POST.get('quantity', '')

        try:
            with transaction.atomic():
                cart = Cart.objects.filter(state=0, userid=user).first()
                if cart is None:
                    print("Create new cart")
                    cart = Cart.objects.create(state=0, userid=user)
                print("cartid:", cart.id)
                cartitem = CartItem.objects.filter(itemid=item, cartid=cart).first()
                if cartitem is None:
                    cartitem = CartItem.objects.create(quantity=quanti, cost=item.outprice, cartid=cart, itemid=item)
                else:
                    CartItem.objects.filter(itemid=item, cartid=cart).update(quantity=cartitem.quantity + int(quanti),
                                                                             cost=item.outprice)

                print("cartitemid:", cartitem.id)

        except Exception as e:
            print(e)
            print("add to cart faild")

        return redirect('/product/detail/' + item_id)


    cartitems = request.POST.getlist('cartitemid', '')
    quantitys = request.POST.getlist('quantity', '')
    try:
        with transaction.atomic():
            for idx, cartitem in enumerate(cartitems):
                print("cartitem:", cartitem)
                print("quantity:", quantitys[idx])

                CartItem.objects.filter(id=cartitem).update(quantity=quantitys[idx])

    except Exception as e:
        print(e)
        print("docartitem faild")

    if request.POST.get("proceed") == "Checkout":
        return redirect('/order/checkout')
    else:
        return redirect('/cart')