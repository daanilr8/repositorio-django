from django.db import models
import json

cuestiones_dict = {
    "Facil": 0,
    "Intermedio": 0,
    "Dificil": 0
}
cuestiones_json = json.dumps(cuestiones_dict)

# Create your models here.



class Cuestiones(models.Model):
    pregunta= models.CharField(max_length = 500)
    opciones = models.JSONField()
    respuesta = models.CharField(max_length = 100)
    dificultad = models.CharField(max_length = 20,null=True,blank=True)
    topic = models.CharField(max_length = 20,null=True,blank=True)
    
class Jugadores(models.Model):
    nombre = models.CharField(max_length=30,primary_key=True)
    contraseña = models.CharField(max_length=30,default="sin_contraseña")
    partidas_jugadas = models.JSONField(null=True,blank=True)
    cuestiones_jugadas = models.JSONField(null=True,blank=True,default=cuestiones_json)
    cuestiones_acertadas = models.JSONField(null=True,blank=True,default=cuestiones_json)
class TopicsExtra(models.Model):
    nombre = models.CharField(max_length=30,primary_key=True)