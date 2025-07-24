"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# Configuración principal de URLs del proyecto
# Define los puntos de entrada globales y montaje de aplicaciones

urlpatterns = [
    # Endpoint base para la API del blog
    path(
        "api/blog/",  # Prefijo para todas las URLs del blog
        include("apps.blog.urls"), 
        # namespace='blog'  # Opcional para namespacing avanzado
    ),
    # Interface de administración Django
    path(
        "admin/",  # Ruta estándar para el admin
        admin.site.urls,
    ),
]

# Configuración para servir archivos estáticos en desarrollo
urlpatterns += static(
    settings.STATIC_URL,  # Prefix para URLs estáticos (ej: /static/)
    document_root=settings.STATIC_ROOT,  # Directorio físico de archivos
)

# Configuración para servir archivos multimedia en desarrollo
urlpatterns += static(
    settings.MEDIA_URL,  # Prefix para medios (ej: /media/)
    document_root=settings.MEDIA_ROOT,  # Directorio físico de uploads
)
