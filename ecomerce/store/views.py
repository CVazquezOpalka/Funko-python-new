from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.conf import settings

# Create your views here.


def index(request):
    # Obtener un producto aleatorio de cada colección
    starwars = Producto.objects.filter(coleccion_id=1).order_by("?").first()
    pokemon = Producto.objects.filter(coleccion_id=2).order_by("?").first()
    hp = Producto.objects.filter(coleccion_id=3).order_by("?").first()
    fecha_actual = datetime.now()
    # Calcular la fecha hace un mes
    fecha_un_mes_atras = fecha_actual - timedelta(days=30)
    # Filtrar los productos agregados en el último mes
    productos_recientes = Producto.objects.filter(
        creado__range=[fecha_un_mes_atras, fecha_actual]
    )
    # Asegurarse de que al menos haya un producto en cada colección
    if starwars is None:
        starwars = Producto.objects.filter(coleccion_id=1).first()
    if pokemon is None:
        pokemon = Producto.objects.filter(coleccion_id=2).first()
    if hp is None:
        hp = Producto.objects.filter(coleccion_id=3).first()

    productos_muestra = [starwars, pokemon, hp]

    context = {"productos": productos_muestra, "productos_nuevos": productos_recientes}

    return render(request, "index.html", context)


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

    listado_productos = Producto.objects.all().order_by("-creado")
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


def lista_de_productos(request):
    lista = list(Producto.objects.all().values_list("name", flat=True))
    if request.method == "GET":
        return JsonResponse(lista, safe=False)


def buscar_producto(request):
    if request.method == "POST":
        search_terms = request.POST.get("buscarproducto")
        if search_terms == "":
            return JsonResponse({"status": "Debes agregar el nombre del producto"})
        else:
            producto_encontrado = Producto.objects.filter(
                name__contains=search_terms
            ).first()
            if producto_encontrado is None:
                return JsonResponse({"status": "No se encontro el producto solicitado"})
            else:
                return redirect(
                    "shop/"
                    + producto_encontrado.coleccion.name
                    + "/"
                    + producto_encontrado.name
                )
    return redirect("shop")


# Stripe
def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
