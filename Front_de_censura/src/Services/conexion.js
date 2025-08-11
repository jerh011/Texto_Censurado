const baseUrl = "http://127.0.0.1:5000/censurado/";

const conexion = async (texto) => {
  try {
    const url = baseUrl + encodeURIComponent(texto || "");
    const resp = await fetch(url);
    if (!resp.ok) throw new Error("Error en la petición");
    return await resp.json();
  } catch (err) {
    console.error("Hubo un problema:", err);
    throw err;
  }
};

export default conexion;
