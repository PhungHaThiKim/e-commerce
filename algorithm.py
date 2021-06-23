from cart.models import CartItem
from product.models import Item
from user.models import Logsearch, Logviewdetail


def processAprioriAlgorithm(item: Item):
    rs_items = []
    process_items = []
    items = Item.objects.all()

    # #Taking only item care to suggest
    # for it in items:
    #     if item.id != it.id:
    #         process_items.append(it)

    #Checking items in carts are ordered
    carts_process = []
    cartitems = CartItem.objects.filter(itemid=item)
    for ci in cartitems:
        if ci.cartid.state == 1:
            carts_process.append(ci.cartid)
    items_process = []
    for c in carts_process:
        lcartitems = CartItem.objects.filter(cartid=c)
        for ci in lcartitems:
            i = ci.itemid
            if i.id != item.id:
                items_process.append(i)
    print("Item buy len=", len(items_process))
    items_process.sort(key=lambda i: i.id, reverse=True)
    print(items_process)

    #process caculate frequency each item 3
    items_frequency = []
    for it in items_process:
        if len(items_frequency) == 0 or items_frequency[len(items_frequency)-1]['item'].id != it.id:
            items_frequency.append(
                {
                    "item": it,
                    "frequency": 1,
                    "support_search": 0,
                    "support_detail": 0,
                    "support_cart": 0,
                    "p": 0.0
                }
            )
        else:
            items_frequency[len(items_frequency)-1]["frequency"] += 1
    print(items_frequency)

    #logsearch 4
    log_search = Logsearch.objects.all()
    ilog = []
    for l in log_search:
        ils = l.content.split(";")
        for i in ils:
            ilog.append(i)

    log_detail = Logviewdetail.objects.all()
    idetail = []
    for l in log_detail:
        ils = l.content.split(";")
        for i in ils:
            idetail.append(i)

    totalcart = CartItem.objects.count()

    # Support search:
    for itf in items_frequency:
        for il in ilog:
            if str(itf["item"].id) == il:
                itf["support_search"] += 1

    # Support detail:
    for itf in items_frequency:
        for ide in idetail:
            if str(itf["item"].id) == ide:
                itf["support_detail"] += 1

    #Support cart:
    for itf in items_frequency:
        cis = CartItem.objects.filter(itemid=itf["item"])
        for ci in cis:
            if ci.cartid.state == 0:
                itf["support_cart"] += 1

    # Cacuplate P(A|B) - weight_search = 0.15, weight_detail = 0.15, weight_cart = 0.7
    total = len(items_process)
    for itf in items_frequency:
        nomal = itf["frequency"] / total
        ps = itf["support_search"] / len(ilog)
        pd = itf["support_detail"] / len(idetail)
        pc = itf["support_cart"] / totalcart
        appears = ps + pd + pc
        if appears != 0:
            itf["p"] = nomal/(ps*0.15+pd*0.15+pc*0.7)
        else:
            itf["p"] = 99999

    items_frequency = sorted(items_frequency, key=lambda i: i['p'], reverse=True)
    print("Frequency", items_frequency)

    for itf in items_frequency:
        rs_items.append(itf['item'])

    return rs_items