from django.urls import path
from . import views
from store.controllers import auth, cart, wishlist


urlpatterns = [
    path("", views.index, name="home"),
    path("registrarse/", auth.registrar, name="registrar"),
    path("iniciar_sesion/", auth.iniciar_sesion, name="iniciarsesion"),
    path("cerrar_sesion/", auth.cerrar_sesion, name="cerrarsesion"),
    path("shop/", views.shop, name="shop"),
    path("shop/<str:categori>/", views.ver_coleccion, name="vercoleccion"),
    path("shop/<str:cat>/<str:nom>", views.vista_producto, name="verproducto"),
    path("carrito_de_compras/", cart.ver_carrito, name="carrito"),
    path("agregar-al-carrito", cart.agregar_al_carrito),
    path("borrar-del-carrito", cart.remover_del_carrito),
    path("favoritos/", wishlist.wishlist, name="favoritos"),
    path("agregar-a-la-lista/", wishlist.agregar_producto_lista),
]
