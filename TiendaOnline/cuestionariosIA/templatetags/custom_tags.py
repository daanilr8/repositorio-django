from django import template

register = template.Library()

@register.filter
def get_item(lista, indice):
    try:
        return lista[indice]
    except IndexError:
        return None
