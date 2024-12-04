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
- No tener ocupados los puertos 30000 y 30001 de las redes de TKGs

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
### Uso de la API de spotify:
Debera de crear un archivo denominado **spotify-auth.yaml** dentro de la carpeta backend 
y popular los cmapos client_id y client_secret. Para obtenerlos consulta la documentación de spotify https://developer.spotify.com/
 ```yaml
spotify:
  client_id: "TU_CLIENT_ID"
  client_secret: "TU_CLIENT_SECRET"
  redirect_uri: "http://localhost:9443/callback"
  scope: "playlist-modify-public"
 ```
### Mapeo de ruta a el archivo spotify-auth.yaml:
Debe colocar la ruta absoluta de el archivo spotify-auth.yaml en el espacio corresponidente del
archivo de configuración del backend de kubernetes
 ```yaml
      volumes:
         - name: spotify-auth-volume
           hostPath: # Cambiar según tus necesidades
              path: /tu/path/aqui/spotify-auth.yaml
              type: File

 ```

### Aplicar las configuraciones:
Situese bajo la carpeta MoodBeats pero por encima ed Kubernetes y ejecute los siguientes comandos las imagenes
se descargaran automaticamente de dockerhub
```bash
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
```
### Monitoreo de los PODs:
Utilice los siguientes comandos para moniotrear la salud de los servicios

```bash
kubectl get pods
kubectl get services
```

## Ejecución

- Ingresar `localhost:30000` en el navegador para acceder a la app.
