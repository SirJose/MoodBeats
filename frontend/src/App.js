import React, { useState } from "react";
import Form from "./components/Form";
import Playlist from "./components/Playlist";

const App = () => {
  const [songs, setSongs] = useState([]);
  const [emotion, setEmotion] = useState("");

  const handleAnalyzeEmotion = async ({ text, model }) => {
    try {
      const response = await fetch("http://backend-service:9443/analyze_emotion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, model }),
      });
      const data = await response.json();
      setEmotion(data.emotion);

      // Obtener canciones para la emoción detectada
      const playlistResponse = await fetch(
        "http://backend-service:9443/create_spotify_playlist",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ emotion: data.emotion }),
        }
      );
      const playlistData = await playlistResponse.json();
      setSongs(playlistData);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h1>MoodBeat</h1>
      <Form onAnalyzeEmotion={handleAnalyzeEmotion} />
      {emotion && <h3>Emoción detectada: {emotion}</h3>}
      <Playlist songs={songs} />
    </div>
  );
};

export default App;
