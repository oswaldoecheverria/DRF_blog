from django.utils import timezone
from django.db import models
from django.utils.text import slugify

import uuid


def blog_thumbnail_directory(instance, filename):
    """Genera la ruta de almacenamiento dinámica para las imágenes de los posts.

    Args:
        instance: Instancia del modelo Post al que pertenece la imagen
        filename: Nombre original del archivo subido

    Returns:
        str: Ruta de almacenamiento en formato 'blog/titulo_del_post/filename.ext'
    """
    return "blog/{0}/{1}".format(instance.title, filename)


def category_thumbnail_directory(instance, filename):
    """Genera la ruta de almacenamiento para imágenes de categorías.

    Similar a blog_thumbnail_directory pero para categorías, usando el nombre de la categoría
    como directorio base.

    Args:
        instance (Category): Instancia del modelo Category
        filename (str): Nombre del archivo de imagen

    Returns:
        str: Ruta en formato 'blog_categories/nombre_categoria/filename.ext'
    """
    return "blog_categories/{0}/{1}".format(instance.name, filename)


class Category(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text="Identificador único universal (UUID)",
    )

    parent = models.ForeignKey(
        "self",
        related_name="children",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Categoría padre",
        help_text="Categoría superior en la jerarquía (opcional)",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Nombre interno",
        help_text="Nombre de referencia para la categoría (máx. 255 caracteres)",
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Título público",
        help_text="Título mostrado a los usuarios (opcional)",
    )

    description = models.TextField(
        verbose_name="Descripción",
        blank=True,
        null=True,
        help_text="Explicación detallada del propósito de esta categoría",
    )

    thumbnail = models.ImageField(
        upload_to=category_thumbnail_directory,
        blank=True,
        null=True,
        verbose_name="Imagen destacada",
        help_text="Imagen principal del post (se almacena en category_thumbnail_directory)",
    )

    slug = models.CharField(
        max_length=128,
        verbose_name="Slug",
        help_text="Identificador URL-amigable (máx. 128 caracteres)",
    )

    def __str__(self):
        """Representación legible de la categoría.

        Returns:
            str: Nombre de la categoría
        """
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]


class Post(models.Model):
    """Modelo que representa un artículo/post del blog.

    Atributos:
        title: Título del post (max 128 caracteres)
        description: Breve descripción/resumen (max 256 caracteres)
        content: Contenido completo del post (texto ilimitado)
        thumbnail: Imagen destacada del post
        keywords: Palabras clave para SEO (max 128 caracteres)
        slug: URL amigable del post (max 128 caracteres)
        status: Estado de publicación (draft/published)
        created_at: Fecha de creación (automática)
        updated_at: Fecha de última modificación (automática)
    """

    class PostObjects(models.Manager):
        """Manager personalizado que filtra solo posts publicados."""

        def get_queryset(self):
            """Sobrescribe el queryset base para filtrar por status=published.

            Returns:
                QuerySet: Contiene solo posts con status='published'
            """
            return super().get_queryset().filter(status="published")

    # Opciones para el campo status
    status_options = (
        ("draft", "Draft"),  # Borrador (no visible públicamente)
        ("published", "Published"),  # Publicado (visible)
    )

    # Campos del modelo
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text="Identificador único universal (UUID)",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Categoría",
        help_text="Categoría temática a la que pertenece este post",
    )

    title = models.CharField(
        max_length=128,
        verbose_name="Título",
        help_text="Título del post (máx. 128 caracteres)",
    )

    description = models.CharField(
        max_length=256,
        verbose_name="Descripción",
        help_text="Breve descripción del post (máx. 256 caracteres)",
    )

    content = models.TextField(
        verbose_name="Contenido",
        help_text="Contenido completo del post en formato HTML/Markdown",
    )

    thumbnail = models.ImageField(
        upload_to=blog_thumbnail_directory,
        verbose_name="Imagen destacada",
        help_text="Imagen principal del post (se almacena en blog/titulo/filename)",
    )

    keywords = models.CharField(
        max_length=128,
        verbose_name="Palabras clave",
        help_text="Palabras clave separadas por comas para SEO",
    )

    slug = models.CharField(
        max_length=128,
        verbose_name="Slug",
        help_text="URL amigable para el post (máx. 128 caracteres)",
        unique=True,  # Asegura que cada slug sea único
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Fecha de creación",
        help_text="Fecha automática de creación",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
        help_text="Fecha automática de última modificación",
    )

    status = models.CharField(
        max_length=10,
        choices=status_options,
        default="draft",
        verbose_name="Estado",
        help_text="Estado de publicación del post",
    )

    # Managers
    objects = models.Manager()  # Manager por defecto (todos los posts)
    postobjects = PostObjects()  # Manager personalizado (solo posts publicados)

    class Meta:
        """Configuración de metadatos del modelo."""

        ordering = ("status", "-created_at")  # Orden por defecto: más reciente primero
        

    def __str__(self):
        """Representación legible del modelo.

        Returns:
            str: Título del post
        """
        return self.title


class Heading(models.Model):
    """Representa los encabezados (títulos) dentro del contenido de un post.

    Permite estructurar el contenido jerárquicamente y generar índices automáticos.
    Cada heading está asociado a un post y tiene un nivel (h1-h6) y orden específico.

    Attributes:
        id (UUID): Identificador único
        post (ForeignKey): Post al que pertenece este encabezado
        title (str): Texto del encabezado
        slug (str): Versión URL-amigable del título
        level (int): Nivel jerárquico (1-6 correspondiente a h1-h6)
        order (int): Orden de aparición en el post
    """

    LEVEL_CHOICES = (
        (1, "H1 - Título principal"),
        (2, "H2 - Subtítulo importante"),
        (3, "H3 - Subtítulo"),
        (4, "H4 - Subtítulo menor"),
        (5, "H5 - Subtítulo pequeño"),
        (6, "H6 - Subtítulo mínimo"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text="Identificador único universal (UUID)",
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.PROTECT,
        related_name="headings",
        verbose_name="Post",
        help_text="Post al que pertenece este encabezado",
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Texto del encabezado",
        help_text="Contenido textual del título (máx. 255 caracteres)",
    )

    slug = models.CharField(
        max_length=255,
        verbose_name="Slug",
        help_text="Versión URL-amigable del título (generado automáticamente)",
    )

    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        verbose_name="Nivel jerárquico",
        help_text="Nivel de importancia (1-6 correspondiente a h1-h6)",
    )

    order = models.PositiveIntegerField(
        verbose_name="Orden de aparición",
        help_text="Número que determina la posición relativa en el post",
    )

    class Meta:
        verbose_name = "Encabezado"
        verbose_name_plural = "Encabezados"
        ordering = ["order"]  # Orden ascendente por defecto
        unique_together = [["post", "slug"], ["post", "order"]]  # Restricciones únicas

    def save(self, *args, **kwargs):
        """Sobrescribe el método save para generar automáticamente el slug.

        Si no se proporciona un slug, se genera uno a partir del título
        usando la función slugify de Django.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        """Representación legible del encabezado.

        Returns:
            str: Formato '[Post Title] > H1: Encabezado'
        """
        return f"{self.post.title} > H{self.level}: {self.title}"
