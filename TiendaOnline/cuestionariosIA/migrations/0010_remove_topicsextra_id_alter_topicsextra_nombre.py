# Generated by Django 5.0.6 on 2024-06-24 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuestionariosIA', '0009_topicsextra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topicsextra',
            name='id',
        ),
        migrations.AlterField(
            model_name='topicsextra',
            name='nombre',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
