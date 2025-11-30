from django.contrib import admin
from .models import Livro, ComentarioLeitura, Avaliacao, ProgressoLeitura, Conversa, Mensagem


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "genero", "em_alta")
    search_fields = ("titulo", "autor")
    list_filter = ("genero", "em_alta")

    fieldsets = (
        ("Informações Gerais", {
            "fields": ("titulo", "autor", "genero", "capa", "em_alta")
        }),
        ("Conteúdo", {
            "fields": ("sinopse", "ficha_tecnica", "conteudo")
        }),
    )

@admin.register(ComentarioLeitura)
class ComentarioLeituraAdmin(admin.ModelAdmin):
    list_display = ("livro", "posicao_paragrafo", "data")
    search_fields = ("livro__titulo",)

admin.site.register(Conversa)
admin.site.register(Mensagem)