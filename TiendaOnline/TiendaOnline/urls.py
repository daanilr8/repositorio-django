"""
URL configuration for TiendaOnline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gestionPedidos import views
from cuestionariosIA import views as views2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seleccionar_app/',views2.seleccionar_app),
    path('cuestiones/',views2.inicio),
    path('pedir_topic/',views2.pedir_topic_y_dificultad,name="vista_pedir_topic"),
    path('pedir_preguntas/',views2.pedir_preguntas),
    path('crear_cuestionario/',views2.crear_cuestionario),
    path('guardar_topic/',views2.guardar_topic),
    path('cuestiones/seleccionar_jugador/<str:error_crear>/<str:error_contraseña>/',views2.seleccionar_jugador,name='vista_seleccionar_jugador'),
    path('comprobar/',views2.comprobar),
    path('cuestionario/',views2.cuestionario,name='vista_cuestionario'),
    path('jugar/',views2.jugar),
    path('mostrar_resultado/',views2.mostrar_resultado),
    path('ranking/',views2.ranking),
    path('busqueda_productos/', views.busqueda_producto),
    path('ver_producto/',views.ver_producto),
    path('buscar/',views.buscar),
    path('home/',views.comprar_producto),
    path('comprar/',views.comprar),
    path('confirmacion/',views.confirmacion),
    path('contacto/',views.contacto),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
