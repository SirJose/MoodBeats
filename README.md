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

### Construir las imágenes (OPCIONAL):
Si eliges compilar tus propiras imagenes debes hacer un push hacia docker hub y podteriormente editar los archivos de deployment
de kubernetes ubicados en la carpeta "kubernetes" del proyecto. A continuación un ejemolo del 
parametro a modificar dentro del spec.
```yaml
    spec:
      containers:
        - name: backend
          image: <nombre de tu imagen en dockerhub>
```
 ```bash
 docker build -t backend-app ./backend
 docker build -t frontend-app ./frontend
 ```
### Uso de la API de spotify:
Debera de crear un archivo denominado **spotify-auth.yaml** dentro de la carpeta backend 
y popular los cmapos client_id y client_secret. Para obtenerlos consulta la documentación de spotify https://developer.spotify.com/. 
Dentro del portal de spotify developers asegurate de colocar **http://localhost:30001/callback** como redirect uri en la aplicación que creaste en el portal
 ```yaml
spotify:
  client_id: "TU_CLIENT_ID"
  client_secret: "TU_CLIENT_SECRET"
  redirect_uri: "http://localhost:30001/callback"
  scope: "playlist-modify-public"
 ```
### Token de autenticación:
Ejecute el notebook **login-token.ipnyb** para generar el token de autenticación 

### Mapeo de ruta a el archivo spotify-auth.yaml y token.json:
Debe colocar la ruta absoluta de el archivo spotify-auth.yaml en el espacio corresponidente del
archivo de configuración del backend de kubernetes
 ```yaml
      volumes:
         - name: spotify-auth-volume
           hostPath: # Cambiar según tus necesidades
              path: /tu/path/aqui/spotify-auth.yaml
              type: File
         - name: tokens-volume
           hostPath:
               path: /tu/path/aqui/MoodBeats/tokens.json
               type: File

 ```

### Aplicar las configuraciones:
Situese bajo la carpeta MoodBeats pero por encima ed Kubernetes y ejecute los siguientes comandos las imagenes
se descargaran automaticamente de dockerhub
```bash
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/frontend-deployment.yaml
```

si por alguna razón no se inicia la descarga de las imagenes de docker puede iniciarlas manualmente con: 

```bash
docker pull diegobran16/frontend-app:v5.0   
docker pull  diegobran16/backend-app:v13.0   
```

### Monitoreo de los PODs:
Utilice los siguientes comandos para moniotrear la salud de los servicios

```bash
kubectl get pods
kubectl get services
```

## Ejecución

- Ingresar `localhost:30000` en el navegador para acceder a la app.
