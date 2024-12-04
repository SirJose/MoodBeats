import React, { useState } from "react";

const Form = ({ onAnalyzeEmotion }) => {
  const [text, setText] = useState("");
  const [model, setModel] = useState("pretrained");

  const handleSubmit = (e) => {
    e.preventDefault();
    onAnalyzeEmotion({ text, model });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>¿Cómo te sientes hoy?</h2>
      <textarea
        placeholder="Escribe aquí tu estado de ánimo..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        required
      />
      <div>
        <label>
          <input
            type="radio"
            name="model"
            value="pretrained"
            checked={model === "pretrained"}
            onChange={() => setModel("pretrained")}
          />
          Modelo Pre-entrenado
        </label>
        <label>
          <input
            type="radio"
            name="model"
            value="custom"
            onChange={() => setModel("custom")}
          />
          Modelo Personalizado
        </label>
      </div>
      <button type="submit">Analizar Emoción</button>
    </form>
  );
};

export default Form;
