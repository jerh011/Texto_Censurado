import "./App.css";
import conexion from "./Services/conexion.js";
import { useState } from "react";

function App() {
  const [texto, setTexto] = useState("");
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const censurar = async () => {
    try {
      setCargando(true);
      setError("");
      const data = await conexion(texto);
      setResultado(data);
      console.log("Datos recibidos:", data);
    } catch (err) {
      setError("No se pudo censurar el texto.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <>
      <div className="titulo">Censurar texto</div>
      <div className="center">
        <div className="containers">
          <div className="derechaizquierda">
            <h2>Texto original</h2>
            <textarea
              placeholder="Escribe el texto aquí"
              value={texto}
              onChange={(e) => setTexto(e.target.value)}
            />
            <button onClick={censurar} disabled={cargando || !texto.trim()}>
              {cargando ? "Censurando..." : "Censurar"}
            </button>
            {error && <p className="error">{error}</p>}
          </div>

          <div className="derechaizquierda">
            <h2>Texto censurado</h2>
            <textarea
              placeholder="Resultado censurado"
              readOnly
              value={resultado?.Texto_censurado || ""}
            />
            {resultado?.Groserias?.length ? (
              <small>Detectadas: {resultado.Groserias.join(", ")}</small>
            ) : null}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
