from django.urls import path
from .views import PostListView, PostDetailView

# Configuración de URLs para la aplicación blog
# Define los endpoints públicos para acceder a los recursos de posts

urlpatterns = [
    # Endpoint para listado de posts
    path(
        "posts/",  # Ruta relativa /posts/
        PostListView.as_view(),  # Vista basada en clase convertida a vista
        name="post-list",  # Nombre único para referencia interna
    ),
    # Endpoint para detalle de un post específico
    path(
        "post/<str:slug>/",  # Captura el slug como parámetro string
        PostDetailView.as_view(),  # Vista de detalle
        name="post-detail",  # Identificador para reverse URL
    ),
]
