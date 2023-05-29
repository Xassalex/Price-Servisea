from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from products.models import Product

from .models import Basket, BasketItem


def basket_view(request):
    try:
        session_id = request.session["basket_id"]
    except KeyError:
        session_id = None

    if session_id:
        basket = Basket.objects.get(id=session_id)
        context = {"basket": basket}
    else:
        empty_message = "Your basket is currently empty"
        context = {"empty": True, "empty_message": empty_message}

    template = "basket/basket-view.html"
    return render(request, template, context)


def update_basket(request, slug):
    # сеанс истекает через х секунд бездействия
    request.session.set_expiry(1800)
    try:
        quantity = request.GET.get("quantity")
        update_quantity = True
    except ValueError:
        quantity = None
        update_quantity = False


    try:
        session_id = request.session["basket_id"]
    except KeyError:
        new_basket = Basket()
        new_basket.save()
        request.session["basket_id"] = new_basket.id
        session_id = new_basket.id

    basket = Basket.objects.get(id=session_id)

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass

    # тру/фолз
    basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)


    if quantity and update_quantity:
        if int(quantity) <= 0:
            basket_item.delete()
        else:
            basket_item.quantity = quantity
            basket_item.save()
    else:
        pass

    start_total_dns = 0.00
    start_total_mvideo = 0.00
    start_total_regard = 0.00

    for item in basket.basketitem_set.all():
        product_total_dns = float(item.product.price_dns) * item.quantity
        product_total_mvideo = float(item.product.price_mvideo) * item.quantity
        product_total_regard = float(item.product.price_regard) * item.quantity
        start_total_dns += product_total_dns
        start_total_mvideo += product_total_mvideo
        start_total_regard += product_total_regard

    request.session["items_total"] = basket.basketitem_set.count()

    basket.total_dns = start_total_dns
    basket.total_mvideo = start_total_mvideo
    basket.total_regard = start_total_regard

    basket.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
