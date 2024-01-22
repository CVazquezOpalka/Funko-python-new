from django.urls import path
from . import views
from store.controllers import auth


urlpatterns = [
    path("", views.index, name="home"),
    path("registrarse/", auth.registrar, name="registrar"),
    path("iniciar_sesion/", auth.iniciar_sesion, name="iniciarsesion"),
    path("cerrar_sesion/", auth.cerrar_sesion, name="cerrarsesion"),
    path("shop/", views.shop, name="shop"),
    path("shop/<str:categori>/", views.ver_coleccion, name="vercoleccion"),
    path("shop/<str:cat>/<str:nom>", views.vista_producto, name="verproducto"),
]
