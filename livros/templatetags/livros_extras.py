# livros/templatetags/livros_extras.py

from django import template

register = template.Library()

@register.filter
def rangelist(value):
    return range(1, int(value)+1)

@register.filter
def div(pagina_atual, total_paginas):
    try:
        if not total_paginas:
            return 0
        return (pagina_atual / total_paginas) * 100
    except Exception:
        return 0