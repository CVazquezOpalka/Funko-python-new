# Generated by Django 5.0.1 on 2024-01-23 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_lista_de_deseos_creado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lista_de_deseos',
            name='creado',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
