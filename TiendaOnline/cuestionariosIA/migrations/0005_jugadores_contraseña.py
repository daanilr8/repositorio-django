# Generated by Django 5.0.6 on 2024-06-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuestionariosIA', '0004_jugadores'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugadores',
            name='contraseña',
            field=models.CharField(default='sin_contraseña', max_length=30),
        ),
    ]
