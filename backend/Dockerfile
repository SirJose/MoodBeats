# Imagen base
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*


# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias desde requirements.txt
RUN pip install --no-cache-dir flask transformers torch \
        deep-translator joblib pandas spotipy pyyaml flask-cors mlflow

COPY models /app/models
COPY data /app/data
COPY app.py /app

# Exponer puerto de Flask
EXPOSE 9443

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]