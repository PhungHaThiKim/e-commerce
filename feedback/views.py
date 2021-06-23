import json
from types import SimpleNamespace

from django.shortcuts import render

# Create your views here.

from cart.models import CartItem
from feedback.models import Feedback
from product.models import Item, Comment
import requests


def managefeedback(request):
    items = Item.objects.all()
    itemid = request.GET.get("itemid", "")
    item = None
    if itemid != "" and itemid != "0":
        item = Item.objects.get(id=itemid)

    comments = None
    feedbacks = None
    listcomment = ""
    listfeedback = ""
    rate = 0
    if item is not None:
        comments = Comment.objects.filter(itemid=item)
        for c in comments:
            if listcomment != "":
                listcomment += ";"
            content = c.content
            content = content.replace(";", " ")
            listcomment += content

        cartitems = CartItem.objects.filter(itemid=item)
        feedbacks = Feedback.objects.filter(cartitemid__in=cartitems)
        for f in feedbacks:
            rate += f.star
            if listfeedback != "":
                listfeedback += ";"
            content = f.content
            content = content.replace(";", " ")
            listfeedback += content
        if len(feedbacks) > 0:
            rate = int((rate/len(feedbacks))*100)/100
    print("listcomment:", listcomment)
    rscObject = []
    total_pos = 0
    cpos = 0
    if listcomment != "":
        payloadc = {'query': listcomment}
        rsc = requests.get('http://localhost:5000', params=payloadc)
        rscObject = json.loads(rsc.text, object_hook=lambda d: SimpleNamespace(**d))
        for ob in rscObject:
            ob.score = int(ob.score*10000)/100 #
            if ob.label == "POSITIVE":
                cpos += 1
                total_pos += 1
        cpos = int((cpos/len(rscObject))*10000)/100
        print("predict:", rscObject)
    print("listfeedback:", listfeedback)
    rsfObject = []
    fpos = 0
    if listfeedback != "":
        payloadf = {'query': listfeedback}
        rsf = requests.get('http://localhost:5000', params=payloadf)
        rsfObject = json.loads(rsf.text, object_hook=lambda d: SimpleNamespace(**d))
        for ob in rsfObject:
            ob.score = int(ob.score * 10000) / 100
            if ob.label == "POSITIVE":
                fpos += 1
                total_pos += 1
        fpos = int((fpos / len(rsfObject)) * 10000) / 100
        print("predict:", rsfObject)

    if len(rscObject) + len(rsfObject) != 0:
        total_pos = int((total_pos/(len(rscObject) + len(rsfObject)))*10000)/100

    return render(request, 'managefeedback.html', {
        'item': item,
        'items': items,
        'comments': comments, #listcmt
        'feedbacks': feedbacks, #listfb
        'pcom': rscObject, #arraypredict
        'pfee': rsfObject,
        'cpos': cpos, #total
        'fpos': fpos, #total
        'total_pos': total_pos,
        'rate': rate
    })