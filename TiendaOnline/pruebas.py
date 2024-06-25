import openai
import requests
import os

# Configura tu clave de API de OpenAI
openai.api_key = "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"

# Define tu descripción de texto para la imagen
prompt = "Una imagen de un circulo señalando  el primer puesto "

# Realiza la solicitud a la API de DALL-E 3
response = openai.images.generate(
    prompt=prompt,
    n=1,  # Número de imágenes a generar
    size="1024x1024"  # Tamaño de la imagen
)

# Obtén la URL de la imagen generada
image_url = response.data[0].url

# Nombre del archivo para guardar la imagen
image_name = "puesto1.png"


folder_path = "D:\\supra\\Documents\\ProyectoDjango\\TiendaOnline\\media"

# Crear la carpeta si no existe
os.makedirs(folder_path, exist_ok=True)

# Ruta completa del archivo de imagen
file_path = os.path.join(folder_path, image_name)

# Descargar la imagen y guardarla en el archivo
response = requests.get(image_url)
if response.status_code == 200:
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"Imagen guardada en: {file_path}")
else:
    print(f"Error al descargar la imagen: {response.status_code}")