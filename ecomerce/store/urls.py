from django.urls import path
from . import views
from store.controllers import auth, cart, wishlist, pagar, compras


urlpatterns = [
    # Rutas
    path("", views.index, name="home"),
    path("mi_cuenta/", auth.mi_cuenta, name="profile"),
    path("registrarse/", auth.registrar, name="registrar"),
    path("iniciar_sesion/", auth.iniciar_sesion, name="iniciarsesion"),
    path("cerrar_sesion/", auth.cerrar_sesion, name="cerrarsesion"),
    path("shop/", views.shop, name="shop"),
    path("shop/<str:categori>/", views.ver_coleccion, name="vercoleccion"),
    path("shop/<str:cat>/<str:nom>", views.vista_producto, name="verproducto"),
    path("carrito_de_compras/", cart.ver_carrito, name="carrito"),
    path("favoritos/", wishlist.wishlist, name="favoritos"),
    path("pagar/", pagar.index, name="checkout"),
    path("mis-compras/", compras.index, name="miscompras"),
    path("ver-compras/<str:t_no>", compras.view, name="orderview"),
    # Controladores
    path(
        "create-checkout-session",
        pagar.create_checkout_session,
        name="create-checkout-session",
    ),
    path("lista-de-productos", views.lista_de_productos),
    path("buscar_producto", views.buscar_producto, name="buscar_producto"),
    path("agregar-al-carrito", cart.agregar_al_carrito),
    path("borrar-del-carrito", cart.remover_del_carrito),
    path("actualizar-carrito", cart.actualizar_carrito),
    path("agregar-a-la-lista", wishlist.agregar_producto_lista),
    path("borrar-de-favoritos", wishlist.borrar_de_favoritos),
    path("place-order", pagar.placeorder, name="placeorder"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
]
