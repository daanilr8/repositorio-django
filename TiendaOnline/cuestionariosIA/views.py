from django.shortcuts import render,redirect,reverse
from django.db.models import F, Value, IntegerField
from django.db.models.functions import Cast
from django.http import HttpResponse,JsonResponse
from cuestionariosIA.models import Cuestiones,Jugadores, TopicsExtra
import openai
import json
import unicodedata
import random

# Create your views here.
def inicio(request):

  return redirect('vista_seleccionar_jugador',error_contraseña=False,error_crear=False)

def seleccionar_jugador(request,error_contraseña,error_crear):

  error_crear_modificado= error_crear.lower() == 'true'
  error_contraseña_modificado = error_contraseña.lower() == 'true'

  jugadores = Jugadores.objects.all()
  return render(request,"seleccionar_jugador.html",{"jugadores":jugadores,"error_crear":error_crear_modificado,"error_contraseña":error_contraseña_modificado})

def comprobar(request):

  jugador = request.GET.get('jugador')

  if jugador == "null":
    nombre_jugador = request.GET.get('jugador_creado_nombre')
    contraseña_jugador = request.GET.get('jugador_creado_contraseña')
    try: 
      Jugadores.objects.get(nombre=nombre_jugador)
      return redirect('vista_seleccionar_jugador',error_contraseña=False,error_crear=True)
    except Jugadores.DoesNotExist:
      jugador_nuevo = Jugadores(nombre=nombre_jugador,contraseña=contraseña_jugador)
      jugador_nuevo.save()
      request.session['usuario'] = nombre_jugador
      return redirect('vista_cuestionario')
  else:
    jugador_seleccionado = Jugadores.objects.get(nombre=jugador)
    if not jugador_seleccionado.contraseña == request.GET.get('jugador_contraseña'):
      return redirect('vista_seleccionar_jugador',error_contraseña=True,error_crear=False)
    else:
        request.session['usuario'] = jugador_seleccionado.nombre
        return redirect('vista_cuestionario')

def pedir_topic_y_dificultad(request):

  return render(request, "pedir_preguntas.html")


def pedir_preguntas(request):

  topic = request.GET["topic"]
  dificultad = request.GET["dificultad"]

  pedir_preguntas_IA(topic,dificultad)
  
  return redirect('vista_pedir_topic')

def pedir_preguntas_IA(topic,dificultad):
  response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
        {
        "role": "system",
        "content": "Eres un asistente para crear un cuestionario, el usuario te enviara un único Topic y el nivel de dificultad de las preguntas, con ese topic quiero que formules 20 preguntas DIFERENTES de dificiultad indicada por el usuario, para poner un contexto preguntas en dificultad fácil para que alguien sin mucho conocimiento pueda responder, intermedio alguien que tiene algo de conocimiento, dificil alguien que tiene mucho conocimiento sobre el topic, cada pregunta tendrá 4 opciones de la cual una de ellas será la correcta, quiero que me indiques las preguntas, opciones y el resultado correcto en un JSON, de forma que el json tenga este prototipo: { preguntas:[ {pregunta : ...., opciones:..., respuesta_correcta:...}, ... ]} "
      },
      {
        "role": "user",
        "content": "topic:" + topic + ", dificultad:" + dificultad
      }
    ]
  )
  json_data = response.choices[0].message.content
  data = json.loads(json_data)
  preguntas = ""

  for item in data['preguntas']:
    pregunta_chatgpt = item['pregunta']
    pregunta = pregunta_chatgpt
    preguntas += pregunta_chatgpt + ","
    opcion = item['opciones']
    respuesta = item['respuesta_correcta']
    cuestion = Cuestiones(pregunta=pregunta,opciones=opcion,respuesta=respuesta,dificultad=dificultad,topic=topic)
    cuestion.save()

def crear_cuestionario(request):

  topics = request.GET.getlist("topic", None)
  topic_extra = request.GET.get('topic_extra')
  if not topic_extra == "Ninguno":
    topics.append(topic_extra)
  dificultad = request.GET["dificultad"]
  numTopics = len(topics)


  if(numTopics)>10:
    print("Hola")
  else:
    numPreguntas = 10 // numTopics
    i = 10%numTopics

    t=0
    corregir = False

    numPreguntasCuest = 0
    respuestas_marcadas = []

    cuestionario = {}
  for topic in topics:

    if i > 0:
      numPreguntasCuest = numPreguntas+1
      i= i-1
    else:
      numPreguntasCuest = numPreguntas
    
    cuestiones = Cuestiones.objects.filter(topic=topic,dificultad=dificultad)
    if len(cuestiones) == 0:
      pedir_preguntas_IA(topic,dificultad)
      cuestiones = Cuestiones.objects.filter(topic=topic,dificultad=dificultad)
    id_preguntas = random.sample(range(1, len(cuestiones)), numPreguntasCuest)
    for id_pregunta in id_preguntas:
      cuestion = cuestiones[id_pregunta]
      cuestionario['cuestion'+str(t)]={
        'pregunta': cuestion.pregunta,
        'opciones': cuestion.opciones,
        'respuesta_correcta':cuestion.respuesta,
        'dificultad':cuestion.dificultad,
        'topic':cuestion.topic
      }
      t=t+1
  request.session['cuestionario'] = cuestionario
  request.session['dificultad'] = dificultad
  
  #return JsonResponse(cuestionario)
  return render(request,"mostrar_preguntas.html",{"cuestionario":cuestionario,"respuestas_marcadas":respuestas_marcadas,"corregir":corregir})
  

def guardar_topic(request):

  topics_extra = TopicsExtra.objects.all()
  nuevo_topic_nombre = request.GET.get('nuevo_topic')

  nuevo_topic = TopicsExtra(nombre = nuevo_topic_nombre)
  nuevo_topic.save()

  return render(request, "cuestionario.html", {"topics_extra":topics_extra})
  

def cuestionario(request):

  topics_extra = TopicsExtra.objects.all()

  return render(request, "cuestionario.html",{"topics_extra":topics_extra})

def jugar(request):

   corregir = False

   topics = request.GET.getlist("topic",None)
   topic_extra = request.GET.get('topic_extra')
   if not topic_extra == "Ninguno":
    topics.append(topic_extra)
   
   topics_str = ""
   for topic in topics:
    topics_str += topic + ","
   dificultad = request.GET["dificultad"]

   response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
        "role": "system",
        "content": "Eres un asistente para crear un cuestionario, el usuario te enviara diferentes topics y el nivel de dificultad de las preguntas, con esos topics quiero que formules 10 preguntas, cada pregunta tendrá 4 opciones de la cual una de ellas será la correcta, quiero que me indiques las preguntas, opciones y el resultado correcto en un JSON, de forma que el json tenga este prototipo: { preguntas:[ {pregunta : ...., opciones:..., respuesta_correcta:..., dificultad: ...., topic: ....}, ... ]} "
      },
      {
        "role": "user",
        "content": "topics:" + topics_str + " dificultad:" + dificultad
      }
    ]
    )
  
   json_data = response.choices[0].message.content
   data = json.loads(json_data)
   folder_path_text = "D:\\supra\\Documents\\ProyectoDjango\\TiendaOnline\\funcionamiento.txt"

   with open(folder_path_text,'a') as file:
      file.write(json_data)

   respuestas_marcadas= []
   cuestionario = {}
   t=0


  # Iterar sobre las preguntas en el JSON y extraer los valores
   for item in data['preguntas']:
    pregunta = item['pregunta']
    opcion = item['opciones']
    respuesta = item['respuesta_correcta']
    dificultad = item['dificultad']
    topic = item['topic']
    cuestionario['cuestion'+str(t)] = {
      'pregunta':pregunta,
      'opciones':opcion,
      'respuesta_correcta': respuesta,
      'dificultad': dificultad,
      'topic': topic,
    }
    cuestion = Cuestiones(pregunta=pregunta,opciones=opcion,respuesta=respuesta,dificultad=dificultad,topic=topic)
    cuestion.save()
    t=t+1
  
   print(t)
   request.session['cuestionario'] = cuestionario
   request.session['dificultad'] = dificultad

   return render(request,"mostrar_preguntas.html",{"cuestionario":cuestionario,"corregir":corregir,"respuestas_marcadas":respuestas_marcadas})

def remover_tildes(texto):
    # Normaliza el texto a su forma "NFD" (Normalization Form Decomposition)
    # Esto separa los caracteres base de los acentos
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Filtra los caracteres que no son "Mark" (es decir, los acentos)
    texto_sin_tildes = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
    return texto_sin_tildes

def mostrar_resultado(request):


    corregir = True
    cuestionario = request.session.get('cuestionario')
    respuestas = request.session.get('respuestas')
    nombre_jugador = request.session.get('usuario')
    dificultad = request.session.get('dificultad')

    dificultad_sintilde = remover_tildes(dificultad)

    jugador = Jugadores.objects.get(nombre=nombre_jugador)
    
    cuestiones_acertadas = json.loads(jugador.cuestiones_acertadas)
    cuestiones_acertadas_dificultad = int(cuestiones_acertadas.get(dificultad_sintilde))
    cuestiones_jugadas = json.loads(jugador.cuestiones_jugadas)
    cuestiones_jugadas_dificultad = int(cuestiones_jugadas.get(dificultad_sintilde))

    respuestas_marcadas = []
    i=0
    #
    for key,value in cuestionario.items():
      respuesta_marcada = request.GET.get("pregunta"+str(i))
      respuestas_marcadas.append(respuesta_marcada)
      if respuesta_marcada == value['respuesta_correcta']:
        cuestiones_acertadas_dificultad+=1
      cuestiones_jugadas_dificultad+=1
      i+=1

    cuestiones_acertadas[dificultad] = cuestiones_acertadas_dificultad
    cuestiones_jugadas[dificultad] = cuestiones_jugadas_dificultad
    cuestiones_acertadas_json = json.dumps(cuestiones_acertadas)
    jugador.cuestiones_acertadas = cuestiones_acertadas_json
    cuestiones_jugadas_json = json.dumps(cuestiones_jugadas)
    jugador.cuestiones_jugadas = cuestiones_jugadas_json
    jugador.save()
    return render(request,"mostrar_preguntas.html",{"cuestionario":cuestionario,"respuestas_marcadas":respuestas_marcadas,"corregir":corregir})

def ranking(request):

  # Obtener todas las instancias de Jugador
  jugadores = Jugadores.objects.all()

  # Crear una lista de tuplas (jugador, valor_facil)
  jugadores_con_facil = [(jugador, json.loads(jugador.cuestiones_acertadas).get('Facil', 0)) for jugador in jugadores]
  jugadores_con_intermedio = [(jugador, json.loads(jugador.cuestiones_acertadas).get('Intermedio', 0)) for jugador in jugadores]
  jugadores_con_dificil = [(jugador, json.loads(jugador.cuestiones_acertadas).get('Dificil', 0)) for jugador in jugadores]

  # Ordenar la lista por el valor de 'facil' de mayor a menor
  jugadores_ordenados_facil = sorted(jugadores_con_facil, key=lambda x: x[1], reverse=True)
  jugadores_ordenados_intermedio = sorted(jugadores_con_intermedio, key=lambda x: x[1], reverse=True)
  jugadores_ordenados_dificil = sorted(jugadores_con_dificil, key=lambda x: x[1], reverse=True)

  return render(request, "ranking.html", {"jugadores_ordenados_facil":jugadores_ordenados_facil,"jugadores_ordenados_intermedio":jugadores_ordenados_intermedio,"jugadores_ordenados_dificil":jugadores_ordenados_dificil})
    
