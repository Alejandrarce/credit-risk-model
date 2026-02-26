# Usa una imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar herramientas necesarias para el sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos e instalar librerías
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido de tu proyecto al contenedor
COPY . .

# Exponer el puerto de la API (8000)
EXPOSE 8000

# Comando para arrancar la API de FastAPI
CMD ["uvicorn", "src.model_deploy:app", "--host", "0.0.0.0", "--port", "8000"]