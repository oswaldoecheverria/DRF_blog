from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuración personalizada para el modelo Category en el Admin de Django.

    Attributes:
        list_display: Controla qué campos se muestran en la lista de registros
        search_fields: Habilita búsqueda por estos campos
        prepopulated_fields: Genera automáticamente el slug desde el name
        list_filter: Filtros laterales para estos campos
        ordering: Orden por defecto
        readonly_fields: Campos de solo lectura
    """

    list_display = ("name", "title", "parent", "slug")  # Columnas visibles
    search_fields = ("name", "title", "description", "slug")  # Campos buscables
    prepopulated_fields = {"slug": ("name",)}  # Auto-generación de slug
    list_filter = ("parent",)  # Filtros laterales por parent
    ordering = ("name",)  # Orden alfabético por name
    readonly_fields = ("id",)  # Evita edición del ID


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Configuración avanzada para el modelo Post en el Admin.

    Organiza la interfaz con fieldsets, controla listados, búsquedas y más.

    Features:
        - Campos agrupados lógicamente
        - Slug auto-generado desde el título
        - Filtros combinados
        - Orden cronológico inverso
        - Protección de campos sensibles
    """

    list_display = (
        "title",
        "status",
        "category",
        "created_at",
        "updated_at",
    )  # Columnas principales
    search_fields = (
        "title",
        "description",
        "content",
        "keywords",
        "slug",
    )  # Búsqueda full-text
    prepopulated_fields = {"slug": ("title",)}  # Slug automático
    list_filter = (
        "status",
        "category",
        "updated_at",
    )  # Filtros combinados
    ordering = ("-created_at",)  # Orden descendente por fecha
    readonly_fields = ("id", "created_at", "updated_at")  # Campos bloqueados

    fieldsets = (
        (
            "General Information",
            {
                "fields": (
                    "title",
                    "description",
                    "content",
                    "thumbnail",
                    "keywords",
                    "slug",
                    "category",
                )
            },
        ),
        (
            "Status & Dates",
            {
                "fields": (
                    "status",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
