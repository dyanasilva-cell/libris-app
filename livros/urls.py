from django.urls import path
from . import views
from . import autenticacao_views

# Esta linha define o namespace 'livros' usado no HTML (livros:home, livros:detalhe_livro)
app_name = 'livros' 

urlpatterns = [
    # -------------------------------------------------------------
    # A. ROTAS DE AUTENTICAÇÃO (Usam autenticacao_views)
    # -------------------------------------------------------------
    path('registro/', autenticacao_views.registro, name='registro'),
    path('login/', autenticacao_views.login_view, name='login_view'),
    path('logout/', autenticacao_views.logout_view, name='logout_view'),
    
    # -------------------------------------------------------------
    # B. ROTAS PRINCIPAIS & LEITURA (Usam views)
    # -------------------------------------------------------------
    path('', views.home, name='home'),
    path('livro/<int:pk>/', views.detalhe_livro, name='detalhe_livro'),
    path('livro/<int:pk>/avaliacao/adicionar/', views.adicionar_avaliacao, name='adicionar_avaliacao'),
    
    # 💡 CORREÇÃO 1: Garanta que você está chamando a função RENOMEADA do views.py.
    # Se você renomeou para 'ler_livro', tem que ser 'views.ler_livro'.
    path('livro/<int:pk>/leitura/', views.ler_livro, name='ler_livro'),
    
    # 💡 CORREÇÃO 2: Garanta que você está chamando a função RENOMEADA do views.py.
    # Se você renomeou para 'publicar_comentario', tem que ser 'views.publicar_comentario'.
    path('livro/<int:pk>/comentario/adicionar/', views.publicar_comentario, name='publicar_comentario'),
    path('perfil/', autenticacao_views.perfil, name='perfil'),
    path('biblioteca/', views.biblioteca, name="biblioteca"),
    path('busca/', views.busca, name='busca'),
    path('chat/', views.chat, name="chat"),
    path("chat/<int:pk>/", views.chat_conversa, name="chat_conversa"),
    path("voz/comando/", views.comando_voz, name="comando_voz"),
]