import React from "react";

const Playlist = ({ songs }) => {
  if (!songs.length) {
    return <p>No hay canciones disponibles para este estado de ánimo.</p>;
  }

  return (
    <div>
      <h2>Playlist Generada</h2>
      <ul>
        {songs.map((song, index) => (
          <li key={index}>
            <strong>{song.track_name}</strong> - {song.artists}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Playlist;
