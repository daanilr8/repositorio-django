# Generated by Django 5.0.6 on 2024-06-20 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuestionariosIA', '0003_rename_diciultad_cuestiones_dificultad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jugadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('partidas_jugadas', models.JSONField(blank=True, null=True)),
                ('cuestiones_jugadas', models.JSONField(blank=True, null=True)),
                ('cuestiones_acertadas', models.JSONField(blank=True, null=True)),
            ],
        ),
    ]
