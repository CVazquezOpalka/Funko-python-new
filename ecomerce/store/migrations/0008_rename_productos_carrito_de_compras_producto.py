# Generated by Django 5.0.1 on 2024-01-23 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_product_carrito_de_compras_productos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carrito_de_compras',
            old_name='productos',
            new_name='producto',
        ),
    ]
