from django.shortcuts import render, redirect
from store.models import Carrito_de_Compras, Producto
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="iniciarsesion")
def ver_carrito(request):
    carrito = Carrito_de_Compras.objects.filter(user=request.user)
    context = {"carrito": carrito}
    return render(request, "cart/index.html", context)


def remover_del_carrito(request):
    if request.method == "POST":
        id_producto = int(request.POST.get("producto_id"))
        if Carrito_de_Compras.objects.filter(
            user=request.user, producto_id=id_producto
        ):
            item = Carrito_de_Compras.objects.filter(
                user=request.user, producto_id=id_producto
            )
            item.delete()
            return JsonResponse({"status": "Producto eliminado"})
    return redirect("home")


def agregar_al_carrito(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            id_producto = int(request.POST.get("producto_id"))
            checkerar_producto = Producto.objects.filter(id=id_producto).first()
            if checkerar_producto:
                if Carrito_de_Compras.objects.filter(
                    user=request.user.id, producto_id=id_producto
                ):
                    print("entro en este if")
                    return JsonResponse(
                        {"status": "el producto ya se encuentra en el carrito"}
                    )
                else:
                    cantidad_solicitada = int(request.POST.get("producto_cantidad"))
                    if checkerar_producto.cantidad >= cantidad_solicitada:
                        Carrito_de_Compras.objects.create(
                            user=request.user,
                            producto_id=id_producto,
                            cantidad_requerida=cantidad_solicitada,
                        )

                        checkerar_producto.cantidad = int(
                            checkerar_producto.cantidad - cantidad_solicitada
                        )
                        checkerar_producto.save()
                        return JsonResponse({"status": "Producto agregado con exito"})
                    else:
                        return JsonResponse(
                            {
                                "status": "Hay "
                                + str(checkerar_producto.cantidad)
                                + " en Stock"
                            }
                        )
            else:
                return JsonResponse({"status": "No se encontro el producto"})
        else:
            return JsonResponse({"status": "Debe iniciar sesíon"})
    return redirect("home")
