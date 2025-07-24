from rest_framework import serializers
from .models import Post, Category, Heading


class PostSerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Post.

    Serializa todos los campos del modelo Post para operaciones CRUD completas.
    Utiliza Meta.fields = "__all__" para incluir automáticamente todos los campos del modelo.

    Notes
    -----
    Campos serializados incluyen:
        - id (UUID): Identificador único del post
        - category (UUID): Referencia a la categoría relacionada
        - title (str): Título del post (128 caracteres máx)
        - description (str): Descripción breve (256 caracteres máx)
        - content (str): Contenido completo en HTML/Markdown
        - thumbnail (ImageField): Ruta de la imagen destacada
        - keywords (str): Palabras clave para SEO
        - slug (str): Identificador URL-amigable único
        - created_at (DateTime): Fecha de creación automática
        - updated_at (DateTime): Fecha de última modificación automática
        - status (str): Estado de publicación ('draft' o 'published')

    Se utiliza en endpoints donde se necesita manipulación completa de posts.
    """

    class Meta:
        model = Post
        fields = "__all__"


class PostListSerializer(serializers.ModelSerializer):
    """Serializer optimizado para listar posts (operaciones de lectura).

    Proporciona un subconjunto de campos del modelo Post para mejorar el rendimiento
    en listados y vistas previas, excluyendo campos pesados como 'content'.

    Attributes
    ----------
    id : UUID
        Identificador único del post
    title : str
        Título del post (128 caracteres máx)
    description : str
        Descripción breve (256 caracteres máx)
    thumbnail : str
        URL de la imagen miniatura
    slug : str
        Identificador URL-amigable
    category : UUID
        Referencia a la categoría relacionada

    Notes
    -----
    - Diseñado específicamente para operaciones de listado donde no se necesita
      el contenido completo del post.
    - Mejora el rendimiento al evitar la serialización del campo 'content' que
      puede ser muy grande.
    - El campo 'category' se serializa como UUID por defecto, pero podría mejorarse
      con anidamiento o slugs según necesidades.
    """

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "thumbnail",
            "slug",
            "category",
        ]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer completo para el modelo Category.

    Serializa todos los campos de categorías incluyendo relaciones jerárquicas.

    Notes
    -----
    Campos serializados incluyen:
        - id (UUID): Identificador único
        - parent (UUID): Referencia opcional a categoría padre (relación recursiva)
        - name (str): Nombre interno de la categoría
        - title (str): Título público (opcional)
        - description (str): Descripción detallada
        - thumbnail (ImageField): Imagen representativa
        - slug (str): Identificador URL-amigable
        - children (list): Lista de categorías hijas (por la relación recursiva)

    La relación 'children' está disponible debido al related_name="children"
    en el modelo, pero no está incluida explícitamente en los fields.
    """

    class Meta:
        model = Category
        fields = "__all__"


class HeadingSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Heading (encabezados dentro de posts).

    Serializa los campos esenciales de los encabezados para construir índices
    o navegación dentro del contenido de un post.

    Attributes
    ----------
    title : str
        Texto del encabezado (255 caracteres máx)
    slug : str
        Versión URL-amigable del título (generada automáticamente)
    level : int
        Nivel jerárquico (1-6 correspondiente a h1-h6)
    order : int
        Posición relativa dentro del post

    Notes
    -----
    - Excluye el campo 'id' y la relación con 'post' para simplificar la respuesta.
    - El campo 'slug' se genera automáticamente del título si no se proporciona.
    - El campo 'level' usa LEVEL_CHOICES definido en el modelo (1-6).
    - El campo 'order' debe ser único dentro de cada post (validado por el modelo).

    Ejemplo de uso:
        - Generar tabla de contenidos automática
        - Navegación entre secciones de un post
        - Anclas para enlaces directos a secciones
    """

    class Meta:
        model = Heading
        fields = [
            "title",
            "slug",
            "level",
            "order",
        ]
