# Generated by Django 5.0.6 on 2024-06-20 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuestiones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.CharField(max_length=500)),
                ('opciones', models.JSONField()),
                ('respuesta', models.CharField(max_length=100)),
            ],
        ),
    ]