# Generated by Django 5.0.1 on 2024-02-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_rating_estrellas'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='puntaje',
            field=models.IntegerField(default=0),
        ),
    ]
