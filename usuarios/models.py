from django.db import models
from django.contrib.auth.models import User # Importa o modelo de usuário padrão do Django

class Perfil(models.Model):
    # Relaciona o Perfil com o usuário padrão (1 para 1)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Informações do Protótipo de Perfil:
    biografia = models.TextField(max_length=500, blank=True, null=True)
    pontuacao = models.IntegerField(default=0)
    livros_lidos = models.IntegerField(default=0) # Para as estatísticas "Lidos"
    avaliacoes_feitas = models.IntegerField(default=0) # Para as estatísticas "Avaliações"
    
    # Campo para armazenar a imagem do perfil (opcional)
    imagem_perfil = models.ImageField(upload_to='perfis/', default='perfis/default.png')

    def __str__(self):
        return f'Perfil de {self.usuario.username}'

# Modelo para a funcionalidade "Seguindo/Seguidores"
class Seguidores(models.Model):
    # Quem está seguindo (o próprio usuário)
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguindo')
    # Quem está sendo seguido
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    
    class Meta:
        verbose_name_plural = "Seguidores" # <-- Adicione esta linha para corrigir o plural!
        unique_together = ('seguidor', 'seguido')

    def __str__(self):
        return f'{self.seguidor.username} segue {self.seguido.username}'