from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from transformers import pipeline
from deep_translator import GoogleTranslator
import pandas as pd
import torch
from transformers import DistilBertTokenizer, DistilBertModel
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yaml
import json
import socket

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar CORS con reglas explícitas
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:30000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Cargar tokens desde archivo JSON
def load_tokens():
    try:
        with open("/app/tokens.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("El archivo 'tokens.json' no existe dentro del contenedor.")
    except json.JSONDecodeError:
        raise ValueError("El archivo 'tokens.json' no contiene un formato válido.")

# Refrescar el token si es necesario
def get_spotify_client():
    tokens = load_tokens()
    sp_oauth = SpotifyOAuth(
        client_id=config['spotify']['client_id'],
        client_secret=config['spotify']['client_secret'],
        redirect_uri=config['spotify']['redirect_uri']
    )
    try:
        token_info = sp_oauth.refresh_access_token(tokens['refresh_token'])
        tokens['access_token'] = token_info['access_token']
        with open("/app/tokens.json", "w") as f:
            json.dump(tokens, f)
    except Exception as e:
        print(f"Error al refrescar el token: {e}")
        raise ValueError("No se pudo autenticar con Spotify. Verifica el archivo 'tokens.json'.")

    return spotipy.Spotify(auth=tokens['access_token'])

# Leer configuración de YAML
def load_config():
    with open("/app/spotify-auth.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

# Cargar modelos y recursos
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
translator = GoogleTranslator(source='es', target='en')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
playlist_model = joblib.load('/app/models/playlist-model/playlist_model.joblib')
classifier = joblib.load('/app/models/sentiment_model/mood_model.joblib')
label_encoder = joblib.load('/app/models/playlist-model/label_encoder.joblib')
scaler = joblib.load('/app/models/playlist-model/scaler.joblib')
songs_library = pd.read_csv('/app/data/songs_library.csv')

# Procesar la librería de canciones
numerical_features = ['popularity', 'danceability', 'energy', 'valence']
songs_library['track_genre'] = label_encoder.transform(songs_library['track_genre'])
songs_library[numerical_features] = scaler.transform(songs_library[numerical_features])
songs_library['mood'] = playlist_model.predict(songs_library[numerical_features + ['track_genre']])

# Función para procesar texto
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www.\S+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    tokens = [word for word in tokens if len(word) > 2]
    return ' '.join(tokens)

# Diccionario de emociones
emotion_translation = {
    "joy": "Alegría",
    "anger": "Enojo",
    "sadness": "Tristeza",
    "fear": "Miedo",
    "surprise": "Sorpresa",
    "love": "Amor",
    "neutral": "Neutral"
}

# Endpoint para analizar emoción
@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    data = request.json
    text = data.get('text', '')
    model_type = data.get('model', 'pretrained')

    if model_type == 'pretrained':
        text_en = translator.translate(text)
        emotion_result = emotion_pipeline([text_en])[0]
        emotion_en = emotion_result['label']
        emotion_es = emotion_translation.get(emotion_en, "otro")
        return jsonify({
            'emotion': emotion_es,
            'confidence': emotion_result['score']
        })
    elif model_type == 'custom':
        text_processed = preprocess_text(text)
        encoded_input = tokenizer(text_processed, return_tensors='pt', padding='max_length', truncation=True, max_length=128)
        with torch.no_grad():
            bert_embeddings = bert_model(**encoded_input).last_hidden_state[:, 0, :].squeeze().numpy()
        emotion_es = classifier.predict([bert_embeddings])[0]
        return jsonify({'emotion': emotion_es})
    else:
        return jsonify({'error': 'Invalid model type'}), 400

# Endpoint para generar playlist
@app.route('/create_spotify_playlist', methods=['POST', 'GET'])
def generate_playlist():
    data = request.json
    emotion = data.get('emotion', '')

    # Filtrar las canciones según la emoción
    playlist_data = songs_library[songs_library['mood'] == emotion].sort_values(
        by='popularity', ascending=False
    ).drop_duplicates(subset=['track_name', 'artists']).head(50)

    if playlist_data.empty:
        return jsonify({'error': f"No songs found for emotion: {emotion}"}), 404

    # Devolver canciones filtradas antes de autenticarse con Spotify
    filtered_songs = playlist_data[['track_name', 'artists']].to_dict(orient='records')

    try:
        # Verificar si el dominio de Spotify es resolvible
        socket.gethostbyname('accounts.spotify.com')

        # Autenticarse y crear la playlist
        sp = get_spotify_client()
        user_id = sp.me()["id"]
        playlist_name = f"Playlist de {emotion.capitalize()}"
        spotify_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)

        track_uris = []
        for _, row in playlist_data.iterrows():
            query = f"{row['track_name']} {row['artists']}"
            search_result = sp.search(q=query, type="track", limit=1)
            if search_result['tracks']['items']:
                track_uri = search_result['tracks']['items'][0]['uri']
                track_uris.append(track_uri)

        if track_uris:
            sp.playlist_add_items(spotify_playlist["id"], track_uris)
            return jsonify({
                'playlist_id': spotify_playlist["id"],
                'playlist_name': playlist_name,
                'songs': filtered_songs,
                'message': f"Playlist '{playlist_name}' creada exitosamente con {len(track_uris)} canciones."
            })
        else:
            return jsonify({'songs': filtered_songs, 'error': "No valid songs found for playlist."}), 404
    except socket.gaierror as e:
        print(f"Error de resolución de DNS: {e}")
        return jsonify({'songs': filtered_songs, 'error': "Error de resolución DNS con Spotify."}), 500
    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({'songs': filtered_songs, 'error': f"Error durante la autenticación o creación de la playlist: {e}"}), 500

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9443)
