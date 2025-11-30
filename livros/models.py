from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# 1. Opções de gênero
GENERO_CHOICES = (
    ('Romance', 'Romance'),
    ('Fantasia', 'Fantasia'),
    ('Ação', 'Ação'),
    ('Ficção Adolescente', 'Ficção Adolescente'),
    ('Contos', 'Contos'),
    ('Drama', 'Drama'),
    ('Gastronomia', 'Gastronomia'),
    ('Espiritualidade', 'Espiritualidade'),
)

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    genero = models.CharField(max_length=100, choices=GENERO_CHOICES)
    sinopse = models.TextField(blank=True, null=True)
    ficha_tecnica = models.TextField(blank=True, null=True)
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)
    em_alta = models.BooleanField(default=False)
    conteudo = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Conteúdo do Livro (Capítulo 1, etc.)"
    )

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    livro = models.ForeignKey(
        Livro, 
        on_delete=models.CASCADE, 
        related_name='avaliacoes'
    )
    nome = models.CharField(max_length=100)
    estrelas = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(1, message="A avaliação deve ter no mínimo 1 estrela."),
            MaxValueValidator(5, message="A avaliação deve ter no máximo 5 estrelas.")
        ]
    )
    texto = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to='avaliacoes/fotos/', blank=True, null=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.nome} - {self.livro.titulo} ({self.estrelas}⭐)"


# 💡 MODELO CORRETO: Este substitui ComentarioPagina e resolve o ImportError
class ComentarioLeitura(models.Model):
    livro = models.ForeignKey(
        Livro, 
        on_delete=models.CASCADE, 
        related_name='comentarios_leitura'
    )
    nome = models.CharField(max_length=100)
    texto = models.TextField()
    # O views.py usa este campo para agrupar comentários por parágrafo
    posicao_paragrafo = models.PositiveIntegerField(default=0) 
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
         ordering = ['data'] 

    def __str__(self):
        return f'Comentário de {self.nome} em "{self.livro.titulo}" (Parágrafo {self.posicao_paragrafo})'

def foto_usuario_path(instance, filename):
    return f'usuarios/{instance.user.id}/{filename}'

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.CharField(max_length=120, blank=True, null=True)
    foto = models.ImageField(upload_to=foto_usuario_path, blank=True, null=True)

    pontos = models.PositiveIntegerField(default=0)
    livros_lidos = models.PositiveIntegerField(default=0)
    livros_publicados = models.PositiveIntegerField(default=0)
    avaliacoes_feitas = models.PositiveIntegerField(default=0)

    def inicial(self):
        return self.user.first_name[0].upper() if self.user.first_name else '?'

    def __str__(self):
        return f"Perfil de {self.user.username}"



class ProgressoLeitura(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leituras'
    )
    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='leituras'
    )
    pagina_atual = models.PositiveIntegerField(default=1)
    total_paginas = models.PositiveIntegerField(default=1)
    atualizado_em = models.DateTimeField(auto_now=True)

    @property
    def progresso_percentual(self):
        if self.total_paginas:
            return round(self.pagina_atual * 100 / self.total_paginas)
        return 0

    class Meta:
        unique_together = ('usuario', 'livro')

    def __str__(self):
        return f'{self.usuario} - {self.livro} ({self.progresso_percentual}%)'


class Conversa(models.Model):
    nome = models.CharField(max_length=120, blank=True, null=True)  # ex: Grupo "Fantasia"
    participantes = models.ManyToManyField(User, related_name="conversas")
    ultimo_update = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.nome or f"Conversa #{self.id}"


class Mensagem(models.Model):
    conversa = models.ForeignKey(
        Conversa,
        on_delete=models.CASCADE,
        related_name="mensagens"
    )
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mensagens"
    )
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    STATUS = (
        ('sent', 'Enviada'),
        ('delivered', 'Entregue'),
        ('read', 'Lida'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='sent')

    def __str__(self):
        return f"{self.autor.username}: {self.texto[:20]}"
