"""
URL configuration for Libris project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota principal (usa o namespace 'livros')
    path('', include('livros.urls', namespace='livros')),
]

# Esta linha é CRUCIAL para servir imagens (capas) em modo de desenvolvimento (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)