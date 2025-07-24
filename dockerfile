FROM python:3.9-slim

# Instalar dependencias del sistema (si son necesarias)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias primero (para cachear la capa)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Puerto expuesto (solo documentación)
EXPOSE 8000

# Comando para ejecutar (debe coincidir con docker-compose.yml)
CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]