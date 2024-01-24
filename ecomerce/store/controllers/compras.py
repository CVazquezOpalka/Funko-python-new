from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import *
from django.contrib.auth.models import User


def index(request):
    order = Oreden_de_pago.objects.filter(user=request.user)
    context = {"order": order}
    return render(request, "compras/index.html", context)


def view(request, t_no):
    order = Oreden_de_pago.objects.filter(traking_no=t_no).filter(user=request.user).first()
    order_items = OrderItems.objects.filter(order=order)
    context = {"orderitems": order_items, "order": order}
    return render(request, "compras/view.html", context)
