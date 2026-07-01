"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Enrutamiento hacia las aplicaciones locales
    path('', include('inicio.urls')),               # Maneja la raíz y páginas estáticas de 'inicio'
    path('dashboard/', include('dashboard.urls')),   # Panel de control del usuario
    path('productos/', include('productos.urls')),   # Catálogo o gestión de productos
]

# Servir archivos multimedia (media) en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)