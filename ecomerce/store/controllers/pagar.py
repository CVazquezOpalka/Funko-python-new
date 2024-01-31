from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from store.models import *
from django.contrib.auth.models import User
import random
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
public_key = settings.STRIPE_PUBLIC_KEY


@login_required(login_url="iniciarsesion")
def index(request):
    carrito = Carrito_de_Compras.objects.filter(user=request.user)
    for item in carrito:
        if item.cantidad_requerida > item.producto.cantidad:
            Carrito_de_Compras.objects.delete(id=item.id)
    items = Carrito_de_Compras.objects.filter(user=request.user)
    total_a_pagar = 0
    for item in items:
        total_a_pagar = total_a_pagar + (item.producto.precio * item.cantidad_requerida)
    userprofile = Profile.objects.filter(user=request.user).first()
    context = {
        "cartitems": items,
        "total_price": total_a_pagar,
        "profile": userprofile,
        "key": public_key,
    }
    return render(request, "pagar.html", context)


@login_required(login_url="login")
def placeorder(request):
    if request.method == "POST":
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get("fname")
            currentuser.last_name = request.POST.get("lname")
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get("phone")
            userprofile.address = request.POST.get("address")
            userprofile.city = request.POST.get("city")
            userprofile.state = request.POST.get("state")
            userprofile.country = request.POST.get("country")
            userprofile.zipcode = request.POST.get("zipcode")
            userprofile.save()

        neworder = Oreden_de_pago()
        neworder.user = request.user
        neworder.fname = request.POST.get("fname")
        neworder.lname = request.POST.get("lname")
        neworder.email = request.POST.get("email")
        neworder.phone = request.POST.get("phone")
        neworder.address = request.POST.get("address")
        neworder.city = request.POST.get("city")
        neworder.state = request.POST.get("state")
        neworder.country = request.POST.get("country")
        neworder.zipcode = request.POST.get("zipcode")
        neworder.fname = request.POST.get("fname")
        neworder.metodo_de_pago = request.POST.get("payment_mode")

        cart = Carrito_de_Compras.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = (
                cart_total_price + item.producto.precio * item.cantidad_requerida
            )

        neworder.precio_total = cart_total_price
        trackno = f"{request.user}" + str(random.randint(1111111, 9999999))
        while Oreden_de_pago.objects.filter(traking_no=trackno) is None:
            trackno = f"{request.user}" + str(random.randint(1111111, 9999999))

        neworder.traking_no = trackno
        neworder.status = "Completed"  # Establecer el estado como "Completed"
        neworder.save()

        neworderitems = Carrito_de_Compras.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItems.objects.create(
                order=neworder,
                product=item.producto,
                price=item.producto.precio,
                quantity=item.cantidad_requerida,
            )

            # to decrece Product into stock
            orderproduct = Producto.objects.filter(id=item.producto_id).first()
            orderproduct.cantidad = orderproduct.cantidad - item.cantidad_requerida
            orderproduct.save()
        # Borramos el carrito
        Carrito_de_Compras.objects.filter(user=request.user).delete()

        payMode = request.POST.get("payment_mode")
        if payMode == "Pagado con Paypal":
            return JsonResponse({"status": "su orden ah sido procesada con exito"})
        else:
            messages.success(request, "tu orden se proceso correctamente")

    return redirect("home")


def create_checkout_session(request):
    # Obtener el usuario actual
    cart_items = Carrito_de_Compras.objects.filter(user=request.user)

    # Construir la lista line_items
    line_items = []
    for item in cart_items:
        line_item = {
            "price_data": {
                "currency": "usd",
                "unit_amount": int(item.producto.precio * 100),  # Convertir a centavos
                "product_data": {"name": item.producto.name},
            },
            "quantity": item.cantidad_requerida,
        }
        line_items.append(line_item)

    # Crear la sesión de pago en Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri("/success/"),
        cancel_url=request.build_absolute_uri("/cancel/"),
    )

    return JsonResponse({"id": session.id})
