from django.shortcuts import render
from django.shortcuts import render, redirect

import algorithm
from cart.models import Cart, CartItem
from feedback.models import Feedback
from order.models import Payment, Shipment
from product.models import Product, Item, Comment, Category, Supplier
from django.http import HttpResponse
from django.contrib import messages
from django.template import Template, Context
from django.db import transaction
from user.models import Fullname, User, Address, Customer, Logsearch, Logviewdetail
# Create your views here.
from user.models import User
import datetime

def index(request):
    search = request.GET.get("search", '')
    litems = []
    items = Item.objects.all()
    if search != "":
        for i in items:
            if i.productid.name.lower().find(search.lower()) != -1 or (i.productid.desc is not None and i.productid.desc.lower().find(search.lower()) != -1):
                litems.append(i)
    else:
        litems = items
    print(len(litems))
    rates = []
    for item in litems:
        cartitems = CartItem.objects.filter(itemid=item)
        feedbacks = Feedback.objects.filter(cartitemid__in=cartitems)
        rate = 0
        for f in feedbacks:
            rate += f.star
        if len(feedbacks) > 0:
            rate = int(rate / len(feedbacks))
        rates.append(rate)

    if "user_id" in request.session.keys():

        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        cus = Customer.objects.get(userid=user)
        cart = Cart.objects.filter(state=0, userid=user).first()
        print("user_id", user)
        if cart is not None:
            cartitems = CartItem.objects.filter(cartid=cart)
            print("cartitems", len(cartitems))
        else:
            cartitems = None

        if search != "":
            content = ""
            for i in litems:
                if content == "":
                    content = str(i.id)
                else:
                    content += ";"+str(i.id)

            timenow = datetime.datetime.now().strftime("%Y-%m-%d")
            log = Logsearch.objects.filter(customeruserid=cus, time=timenow).first()
            try:
                with transaction.atomic():
                    if log is None:
                        Logsearch.objects.create(customeruserid=cus, time=timenow, content=content)
                    else:
                        ct = log.content
                        if content != "":
                            if ct == "":
                                ct = content
                            else:
                                ct += ";"+content
                            Logsearch.objects.filter(id=log.id).update(content=ct)
            except Exception as e:
                print(e)
                print("faild")
    else:
        user = None
        cartitems = None


    return render(request, 'home_view.html', {'items': litems, 'rates': rates, 'user': user, 'cartitems': cartitems})

def manageproduct(request):
    items = Item.objects.all()
    print(len(items))
    addmodel = request.GET.get('add')
    if "user_id" in request.session.keys():
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        cart = Cart.objects.filter(state=0, userid=user).first()
        categorys = Category.objects.all()
        suppliers = Supplier.objects.all()
        print("user_id", user)
        if cart is not None:
            cartitems = CartItem.objects.filter(cartid=cart)
            print("cartitems", len(cartitems))
        else:
            cartitems = None
    else:
        user = None
        cartitems = None

    return render(request,'manageproduct.html', {'items': items,'categorys':categorys,'suppliers':suppliers,
                                                 'user': user, 'cartitems': cartitems, 'addmodel': addmodel})
def productdetail(request, id):
    item = Item.objects.filter(id=id)[0]

    cartitems = CartItem.objects.filter(itemid=item)
    feedbacks = Feedback.objects.filter(cartitemid__in=cartitems)
    rate = 0
    for f in feedbacks:
        rate += f.star
    if len(feedbacks) > 0:
        rate = int(rate / len(feedbacks))

    product = item.productid
    comments = []
    fullname = []
    for c in Comment.objects.filter(itemid=id):
        comments.append(c)

    user_id = request.session["user_id"]
    user = User.objects.get(id=user_id)
    cus = Customer.objects.get(userid=user)
    cart = Cart.objects.filter(state=0, userid=user).first()
    cartitems = CartItem.objects.filter(cartid=cart)
    category = product.categoryid

    items = algorithm.processAprioriAlgorithm(item)

    content = str(item.id)

    timenow = datetime.datetime.now().strftime("%Y-%m-%d")
    log = Logviewdetail.objects.filter(customeruserid=cus, time=timenow).first()
    try:
        with transaction.atomic():
            if log is None:
                Logviewdetail.objects.create(customeruserid=cus, time=timenow, content=content)
            else:
                ct = log.content
                if content != "":
                    if ct == "":
                        ct = content
                    else:
                        ct += ";" + content
                    Logviewdetail.objects.filter(id=log.id).update(content=ct)
    except Exception as e:
        print(e)
        print("faild")

    return render(request, 'productdetail.html',
                  {
                      'items': items,
                      'product': product,
                      'item': item,
                      'comments': comments,
                      'category': category.name,
                      'cartitems': cartitems,
                      'rate': rate
                  })

def deleteProduct(request, id):
    try:
        with transaction.atomic():
            item = Item.objects.get(id=id)
            iditem = item.productid.id
            print(id)
            Item.objects.filter(id=id).delete()
            print(iditem)
            Product.objects.get(id=iditem).delete()
            messages.success(request, "Your item deleted from your cart.")
    except Exception as e:
        print(e)
        print("delete faild")

    return redirect("/product/manageproduct")

def addProduct(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        supplier_id = request.POST.get("supplier_id")
        product_name = request.POST.get("product_name")
        product_image = request.POST.get("product_image")
        product_price = request.POST.get("product_price")
        item_outprice = request.POST.get("item_outprice")
        product_quantity = request.POST.get("product_quantity")
        product_des = request.POST.get("product_des")
        print(category_id, supplier_id, product_name, product_image, product_price,item_outprice, product_quantity, product_des)
        try:
            with transaction.atomic():
                category = Category.objects.get(id = category_id)
                supplier = Supplier.objects.get(id = supplier_id)
                product = Product.objects.create(categoryid=category,
                                        supplierid = supplier,
                                       price=product_price,
                                       quantity=product_quantity,
                                       img=product_image,
                                       name=product_name,
                                       desc=product_des
                                       )
                print(product)
                item = Item.objects.create(productid = product, outprice = item_outprice)
                print(item)

        except Exception as e:

            print(e)
            print("insert faild")

        return redirect("/product/manageproduct")
    else:
        return redirect("/product/manageproduct")

# view category
def managecategory(request):

    addmodel = request.GET.get('add')
    if "user_id" in request.session.keys():
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        payment = Payment.objects.all()
        categories = Category.objects.all()
        suppliers = Supplier.objects.all()
        shipment = Shipment.objects.all()
        print("user_id", user)

    else:
        user = None

    return render(request,'managecategory.html', {'payment': payment,'categories':categories,'suppliers':suppliers,
                                                 'user': user, 'shipment': shipment, 'addmodel': addmodel})

# delete category
def deleteCategory(request, id):
    try:
        with transaction.atomic():
            Category.objects.filter(id=id).delete()

    except Exception as e:
        print(e)
        print("delete faild")

    return redirect("/product/managecategory")

def addCategory(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        try:
            with transaction.atomic():
                if category_id != '0':
                    category_name = request.POST.get("category_name")
                    print(category_id, category_name)

                    category = Category.objects.get(id = category_id)

                    catenew = Category.objects.create(name=category_name,
                                            categoryfather = category_id)
                    print(catenew)
                else:
                    category_name = request.POST.get("category_name")
                    catenew = Category.objects.create(name=category_name)
                    print(catenew)
        except Exception as e:
            print(e)
            print("insert faild")

        return redirect("/product/managecategory")
    else:
        return redirect("/product/managecategory")

def addcomment(request):
    if request.method == "POST":
        user_id = request.session['user_id']
        print('user_id', user_id)
        user = User.objects.get(id=user_id)
        itemID = request.POST.dict()['itemIDcomment']
        content = request.POST.dict()['content']
        time = datetime.datetime.now()
        try:
            with transaction.atomic():
                item = Item.objects.filter(id=int(itemID))[0]
                # user = User.objects.filter(id=int(user))[0]
                Comment.objects.create(userid=user, itemid=item, content=content, time=time, state="New")
        except Exception as e:
            print(e)
            print("add comment faild")

        return redirect('/product/detail/'+itemID)
    else:
        return redirect("/product")
