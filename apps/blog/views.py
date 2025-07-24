from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Post
from .serializers import PostListSerializer, PostSerializer


class PostListView(ListAPIView):
    """Vista para listar posts publicados usando el manager personalizado PostObjects.

    Esta vista implementa un endpoint GET que devuelve una lista paginada de posts
    en estado 'published', utilizando el serializer optimizado PostListSerializer.

    Attributes
    ----------
    queryset : QuerySet
        Conjunto de resultados filtrados por Post.postobjects (solo posts publicados)
    serializer_class : PostListSerializer
        Serializer optimizado para operaciones de listado

    Notes
    -----
    - Utiliza el manager personalizado PostObjects definido en el modelo Post para
      filtrar automáticamente solo posts con status='published'.
    - El queryset no necesita filtros adicionales porque PostObjects ya aplica el
      filtro base.
    - La paginación se controla mediante la configuración DEFAULT_PAGINATION_CLASS
      de DRF.
    - El serializer PostListSerializer excluye el campo 'content' para optimizar
      el rendimiento en listados.

    Ejemplo de respuesta (JSON):
    [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "Título del post",
            "description": "Descripción breve",
            "thumbnail": "/media/blog/titulo-del-post/imagen.jpg",
            "slug": "titulo-del-post",
            "category": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        ...
    ]
    """

    queryset = Post.postobjects.all()
    serializer_class = PostListSerializer


class PostDetailView(RetrieveAPIView):
    """Vista para detalle de un post individual usando PostObjects.

    Implementa un endpoint GET que devuelve todos los campos de un post específico
    identificado por su campo slug, solo si está publicado.

    Attributes
    ----------
    queryset : QuerySet
        Posts publicados (filtrados por Post.postobjects)
    serializer_class : PostSerializer
        Serializer completo con todos los campos del post
    lookup_field : str
        Campo usado para buscar el recurso (slug en lugar del id por defecto)

    Notes
    -----
    - Hereda de RetrieveAPIView para proporcionar automáticamente la operación
      de recuperación por slug.
    - El uso de Post.postobjects garantiza que no se puedan recuperar posts
      en estado 'draft' incluso conociendo el slug.
    - El lookup_field="slug" permite URLs amigables como /posts/mi-titulo-post/
      en lugar de /posts/123/.
    - Incluye todos los campos del post a través de PostSerializer, incluyendo
      el content completo.

    Ejemplo de respuesta (JSON):
    {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "category": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "Tecnología",
            ...
        },
        "title": "Título completo del post",
        "description": "Descripción extendida",
        "content": "<p>Contenido HTML completo...</p>",
        ...
    }
    """

    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
