# Generated by Django 5.0.1 on 2024-01-23 22:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_rename_product_lista_de_deseos_producto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lista_de_deseos',
            name='creado',
        ),
    ]
