from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Coleccion)
admin.site.register(Producto)
admin.site.register(Lista_de_Deseos)
admin.site.register(Carrito_de_Compras)
admin.site.register(Profile)
admin.site.register(Oreden_de_pago)
admin.site.register(OrderItems)
admin.site.register(Comentario)

