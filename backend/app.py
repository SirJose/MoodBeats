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

# Inicializar la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Leer configuración de YAML
def load_config():
    with open("spotify-auth.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config['spotify']['client_id'],
    client_secret=config['spotify']['client_secret'],
    redirect_uri=config['spotify']['redirect_uri'],
    scope=config['spotify']['scope']
))
# Cargar modelos y recursos
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
translator = GoogleTranslator(source='es', target='en')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
playlist_model = joblib.load('models/playlist-model/playlist-model.joblib')
classifier = joblib.load('models/sentiment_model/mood_model.joblib')
label_encoder = joblib.load('models/playlist-model/label_encoder.joblib')
scaler = joblib.load('models/playlist-model/scaler.joblib')
songs_library = pd.read_csv('data/songs_library.csv')

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
@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    data = request.json
    emotion = data.get('emotion', '')

    playlist_data = songs_library[songs_library['mood'] == emotion].sort_values(
        by='popularity', ascending=False
    ).drop_duplicates(subset=['track_name', 'artists']).head(50)

    if not playlist_data.empty:
        return jsonify(playlist_data.to_dict(orient='records'))
    else:
        return jsonify({'error': f'No songs found for emotion: {emotion}'}), 404

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9443)
