import datetime
import json

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .models import *
from .urils import cookieCart

# Create your views here.


def store(request: HttpRequest):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order is None:
            order = Order.objects.create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]

    products = Product.objects.all()
    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order is None:
            order = Order.objects.create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request: HttpRequest):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()
        if order is None:
            order = Order.objects.create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def update_item(request: HttpRequest):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print("Action:", action)
    print("Product Id:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order = Order.objects.filter(customer=customer, complete=False).first()
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    print(orderItem)
    print(orderItem.quantity)
    if action == "add":
        print("Adding item")
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.filter(customer=customer, complete=False).first()
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping:
            ShippingAdress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
            )
    else:
        print("User is not logged in")
    return JsonResponse("Payment complete", safe=False)
