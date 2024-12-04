# MoodBeats

MoodBeats es un proyecto que combina la detección de emociones con la generación de listas de reproducción musicales. Solo escribe como te sientes y MoodBeats se encargará de generar una playlist perfecta para ti!

## Funcionalidades
- Detección de emociones en texto utilizando modelos preentrenados y personalizados.
- Generación dinámica de playlists basadas en emociones detectadas.
- Backend desarrollado en Python.
- Frontend desarrollado en React.
- Soporte para despliegue con Kubernetes y Docker.

## Python Notebooks

1. **`AppWorkflow.ipynb`:**
   - Genera playlists a partir de emociones detectadas en texto.
   - Utiliza un modelo preentrenado y la API de Spotify.

2. **`get_models_save_local.ipynb`:**
   - Permite descargar y guardar modelos desde un servidor MLflow.

3. **`our_emotion_detection.ipynb`:**
   - Entrena un modelo propio para detectar emociones usando embeddings de `DistilBERT`.

4. **`playlistModel.ipynb`:**
   - Explora cómo mapear emociones con generación de playlists.

5. **`pre-trained-emotion-detection.ipynb`:**
   - Detecta emociones en texto traducido al inglés utilizando un modelo preentrenado.

## Requisitos
- Python >= 3.8
- Node.js >= 14
- Docker
- Kubernetes

## Instalación

### Clonar el repositorio
```bash
git clone https://github.com/SirJose/MoodBeats
cd MoodBeats
```

### Construir las imágenes:
 ```bash
 docker build -t backend-app ./backend
 docker build -t frontend-app ./frontend
 ```

### Ejecutar los contenedores:
 ```bash
 docker run -d -p 9443:9443 backend-app
 docker run -d -p 80:80 frontend-app
 ```

### Aplicar las configuraciones:
```bash
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
```


## Ejecución

- Ingresar `localhost:80` en el navegador para acceder a la app.
