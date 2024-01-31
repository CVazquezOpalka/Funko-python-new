from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse

from django.conf import settings

# Create your views here.


def index(request):
    return render(request, "index.html")


def shop(request):
    if request.method == "POST":
        coleccion_nombre = request.POST.get("coleccion")
        if coleccion_nombre:
            # Procesar el formulario cuando se envía
            coleccion = get_object_or_404(Coleccion, name=coleccion_nombre)
            lista_producto = Producto.objects.filter(coleccion=coleccion)
            context = {"productos": lista_producto, "coleccion": coleccion}
            return render(request, "shop/coleccion.html", context)

        else:
            messages.warning(request, "Por favor, selecciona una colección.")
            return redirect("home")

    listado_productos = Producto.objects.all()
    paginado = Paginator(listado_productos, 6)
    pagina = request.GET.get("page") or 1
    productos = paginado.get_page(pagina)
    pagina_actual = int(pagina)
    paginas_totales = range(1, productos.paginator.num_pages + 1)
    coleccion = Coleccion.objects.all()
    context = {
        "productos": productos,
        "coleccion": coleccion,
        "paginas": paginas_totales,
        "pagina_actual": pagina_actual,
    }
    return render(request, "shop/index.html", context)


def ver_coleccion(request, categori):
    coleccion = get_object_or_404(Coleccion, name=categori)
    lista_producto = Producto.objects.filter(coleccion=coleccion)
    context = {"productos": lista_producto, "coleccion": coleccion}
    return render(request, "shop/coleccion.html", context)


def vista_producto(request, cat, nom):
    coleccion = get_object_or_404(Coleccion, name=cat)
    productos_relacionados = Producto.objects.filter(coleccion=coleccion).exclude(
        name=nom
    )
    if Coleccion.objects.filter(name=cat).first():
        if Producto.objects.filter(name=nom):
            producto = Producto.objects.filter(name=nom).first()
            context = {
                "producto": producto,
                "productos_relacionados": productos_relacionados,
            }
            return render(request, "shop/view.html", context)
        else:
            messages.warning(request, "No se encontro el Producto")
            return redirect("home")
    else:
        messages.warning("No se encontro la colección")
        return redirect("home")


# Stripe
def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')


class CreateCheckoutSesionView(View):
    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price-data": {
                        "currency": "usd",
                        "unit_amount": 2000,
                        "product_data": {"name": "El producto"},
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success.html",
            cancel_url=YOUR_DOMAIN + "/cancel.html",
        )
        return JsonResponse({"id": checkout_session.id})
