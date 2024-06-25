from django.db import models

# Create your models here.

class Clients(models.Model):
    nombre = models.CharField(max_length = 30)
    direccion = models.CharField(max_length = 50)
    email = models.EmailField()
    tfno = models.CharField(max_length = 7)

    def __str__(self):
        return self.nombre

class Articulos(models.Model):
    nombre = models.CharField(max_length = 30)
    seccion=models.CharField(max_length = 50)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to="fotos_articulos",null=True,blank=True)
    cantidad = models.IntegerField(default=30)
    enWeb = models.BooleanField(default=False)
    descripcion = models.CharField(max_length = 500, null=True,blank=True)
    riego = models.CharField(max_length=300,null=True,blank=True)
    transplante = models.CharField(max_length=300,null=True,blank=True)
    fertilizante = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return "El nombre del articulo es %s la seccion es %s y el precio es %s" % (self.nombre,self.seccion,self.precio)

class Pedidos(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField()
    entregado = models.BooleanField(default=False)
