# usuarios/admin.py
from django.contrib import admin
from .models import Perfil, Seguidores # Importa os novos modelos
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# 1. Registro do Perfil
admin.site.register(Perfil)

# 2. Registro do modelo Seguidores
admin.site.register(Seguidores)

# Opcional: Integração do Perfil na página de usuário padrão do Django (Recomendado)
class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'
    fk_name = 'usuario'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline,)
    
# Desregistra e registra novamente o modelo User padrão com a nossa personalização
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)