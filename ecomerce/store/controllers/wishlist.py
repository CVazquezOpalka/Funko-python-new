from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Lista_de_Deseos, Producto


@login_required(login_url="iniciarsesion")
def wishlist(request):
    productos = Lista_de_Deseos.objects.filter(user=request.user)
    context = {"productos": productos}
    return render(request, 'favoritos/favoritos.html', context)


def agregar_producto_lista(request):
    pass