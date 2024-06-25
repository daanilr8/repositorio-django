from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from gestionPedidos.models import Articulos,Pedidos,Clients
import os
import requests
import json
import datetime
import openai

openai.api_key = "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"

# Create your views here.

def busqueda_producto(request):
    
    return render(request, "busqueda_producto.html")

def buscar(request):

    if request.GET["prd"]:

        producto = request.GET["prd"]
        articulos = Articulos.objects.filter(nombre__icontains=producto)

        return render(request, "resultado_busqueda.html", {"articulos":articulos,"query":producto})
    else:
        mensaje = "No has introducido ningun articulo"

    return HttpResponse(mensaje)

def comprar_producto(request):

    articulos = Articulos.objects.all()
    
    for articulo in articulos:
        if not articulo.imagen:
            rellenar_imagen(articulo)

    pregunta = False
    respuesta = "Ninguna"

    if 'mensaje' in request.GET:
        pregunta = request.GET["mensaje"]
        response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": pregunta}
    ]
    )
        pregunta = True
        respuesta = response.choices[0].message.content
    return render(request, "comprar_producto.html",{"articulos":articulos,"pregunta":pregunta,"respuesta":respuesta})

def ver_producto(request):

    nombre_articulo = request.GET["articulo_nombre"]
    articulo = Articulos.objects.get(nombre__icontains = nombre_articulo)

    if not(articulo.descripcion and articulo.riego and articulo.fertilizante):
        rellenar(articulo)

    return render(request,"ver_producto.html",{"articulo":articulo})

def rellenar(articulo):

    mensaje="Planta : " + articulo.nombre + ", atributos a conocer :"
    formato=""

    if not articulo.descripcion:
        mensaje+="Descripción "
    if not articulo.riego:
        mensaje +="Riego "
    if not articulo.fertilizante:
        mensaje += "Fertilizante "

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
        "role": "system",
        "content": "Eres un asistente para una página web de flores, necesito que describas con exactitud los atributos de la planta señalados por el usuario, cada atributo debe empezar por su nombre y dos puntos , cada atributo debe contener 100palabras"
      },
      {
        "role": "user",
        "content": mensaje
      }
    ]
    )
    respuesta = response.choices[0].message.content

    # Dividir el texto en secciones utilizando el método split
    secciones = respuesta.split("\n")

    # Iterar sobre las secciones para encontrar y almacenar la información relevante
    for seccion in secciones:
        if seccion.startswith("Descripción:"):
            articulo.descripcion = seccion.replace("Descripción:" , "").strip()
        elif seccion.startswith("Riego:"):
            articulo.riego = seccion.replace("Riego:", "").strip()
        elif seccion.startswith("Fertilizante:"):
            articulo.fertilizante = seccion.replace("Fertilizante:", "").strip()

    articulo.save()


def rellenar_imagen(articulo):
    # Define tu descripción de texto para la imagen
    prompt = "Una flor" + articulo.nombre + "muy bonita en una casa reluciente"

    # Realiza la solicitud a la API de DALL-E 3
    response = openai.images.generate(
        prompt=prompt,
        n=1,  # Número de imágenes a generar
        size="1024x1024"  # Tamaño de la imagen
    )

    # Obtén la URL de la imagen generada
    image_url = response.data[0].url

    # Nombre del archivo para guardar la imagen
    image_name = articulo.nombre+"generadaIA.png"
    text_name = "funcionamiento.txt"


    folder_path = "D:\\supra\\Documents\\ProyectoDjango\\TiendaOnline\\media"
    folder_path_text = "D:\\supra\\Documents\\ProyectoDjango\\TiendaOnline"

    # Crear la carpeta si no existe
    os.makedirs(folder_path, exist_ok=True)

    # Ruta completa del archivo de imagen
    file_path = os.path.join(folder_path, image_name)
    file_path_2 = os.path.join(folder_path_text,text_name)

    # Descargar la imagen y guardarla en el archivo
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(file_path_2,'a') as file:
            file.write("hay URL" + image_url + "\n")
        with open(file_path, 'wb') as f:
            f.write(response.content)
        articulo.imagen = file_path
        articulo.save()
        print(f"Imagen guardada en: {file_path}")
    else:
        with open(file_path_2,'a') as file:
            file.write("no hay URL")
        print(f"Error al descargar la imagen: {response.status_code}")


def comprar(request):

    nombre_articulo = request.GET["articulo_nombre"]
    articulo = Articulos.objects.get(nombre__icontains = nombre_articulo)

    return render(request,"comprar.html",{"articulo":articulo})

def confirmacion(request):


    nombre_articulo =  request.GET["articulo_nombre"]
    articuloModificado = Articulos.objects.get(nombre__icontains=nombre_articulo)
    articuloModificado.cantidad = articuloModificado.cantidad-1
    articuloModificado.save()
    ultimoPedido = Pedidos.objects.latest('numero')
    current_datetime = datetime.datetime.now()
    nuevoPedido = Pedidos(numero=ultimoPedido.numero+1,fecha=current_datetime,entregado=False)
    nuevoPedido.save()


    return render(request,"confirmacion.html")



def contacto(request):

    return render(request, "contacto.html")