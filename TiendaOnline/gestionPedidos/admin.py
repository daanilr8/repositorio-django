from django.contrib import admin

from gestionPedidos.models import Articulos,Clients,Pedidos

# Register your models here.

class ClientsAdmin(admin.ModelAdmin):
    list_display=("nombre","direccion","tfno")
    search_fields=("nombre","tfno")

admin.site.register(Clients,ClientsAdmin)
admin.site.register(Articulos)
admin.site.register(Pedidos)

