from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
import os


# Create your models here.


def get_file_path(request, filename):
    original_filename = filename
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join("uploads/", filename)


class Coleccion(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Producto(models.Model):
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    descripcion = models.TextField(max_length=500, null=False, blank=False)
    img = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    precio = models.FloatField(null=False, blank=False)
    cantidad = models.IntegerField(default=0, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    tendencia = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    tag = models.CharField(max_length=150, null=False, blank=False)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Carrito_de_Compras(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_requerida = models.IntegerField(null=False, blank=False)
    creado = models.DateTimeField(auto_now_add=True)


class Lista_de_Deseos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.producto.name} - {self.creado}"


class Oreden_de_pago(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    zipcode = models.IntegerField(null=False, blank=False)
    precio_total = models.FloatField(null=False)
    metodo_de_pago = models.CharField(max_length=150, null=False)
    pago_id = models.CharField(max_length=250, null=True)
    estado_orden = (
        ("Pending", "Pending"),
        ("Out for shipping", "Out for shipping"),
        ("Completed", "Completed"),
    )
    status = models.CharField(max_length=150, choices=estado_orden, default="Pending")
    message = models.TextField(null=True)
    traking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.traking_no)


class OrderItems(models.Model):
    order = models.ForeignKey(Oreden_de_pago, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return "{} - {}".format(self.order.id, self.order.traking_no)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    zipcode = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
