# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
#COPY . .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir mlflow[extras] gunicorn

# Expon el puerto en el que se ejecutará el servidor de MLflow
EXPOSE 6000

# Comando para ejecutar el servidor de MLflow
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5001", "--backend-store-uri", "sqlite:///mlflow.db", "--default-artifact-root", "/artifacts"]
