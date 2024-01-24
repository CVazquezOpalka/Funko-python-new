from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Lista_de_Deseos, Producto


@login_required(login_url="iniciarsesion")
def wishlist(request):
    productos = Lista_de_Deseos.objects.filter(user=request.user)
    context = {"productos": productos}
    return render(request, "favoritos/favoritos.html", context)


def agregar_producto_lista(request):
    """
    Adds a product to the user's wishlist (Lista de Deseos).
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                id_producto = int(request.POST.get("producto_id"))
                producto = get_object_or_404(Producto, id=id_producto)

                if Lista_de_Deseos.objects.filter(user=request.user, producto=producto):
                    return JsonResponse(
                        {"status": "El producto ya se encuentra en Favoritos"}
                    )
                else:
                    Lista_de_Deseos.objects.create(user=request.user, producto=producto)
                    return JsonResponse({"status": "Producto agregado correctamente"})
            except Producto.DoesNotExist:
                return JsonResponse({"status": "No se encontró el producto"})
        else:
            return JsonResponse({"status": "Debe ingresar al sitio para continuar"})
    return redirect("home")


def borrar_de_favoritos(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            id_producto = int(request.POST.get("producto_id"))
            if Lista_de_Deseos.objects.filter(
                user=request.user, producto_id=id_producto
            ):
                item = Lista_de_Deseos.objects.filter(
                    user=request.user, producto_id=id_producto
                )
                item.delete()
                return JsonResponse({
                    "status":"El producto fue removido de la lista"
                })
            else:
                return JsonResponse(
                    {"status": "El producto no se encuentra en la lista"}
                )
        else:
            return JsonResponse({"status": "Debes iniciar sesion"})
