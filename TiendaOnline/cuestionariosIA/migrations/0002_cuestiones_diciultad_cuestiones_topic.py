# Generated by Django 5.0.6 on 2024-06-20 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuestionariosIA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuestiones',
            name='diciultad',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cuestiones',
            name='topic',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
