import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Crear la raíz para React
const root = ReactDOM.createRoot(document.getElementById("root"));

// Renderizar la aplicación principal
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
