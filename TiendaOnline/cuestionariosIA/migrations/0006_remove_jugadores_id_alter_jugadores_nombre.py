# Generated by Django 5.0.6 on 2024-06-20 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuestionariosIA', '0005_jugadores_contraseña'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jugadores',
            name='id',
        ),
        migrations.AlterField(
            model_name='jugadores',
            name='nombre',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]