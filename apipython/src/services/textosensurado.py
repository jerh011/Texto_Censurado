# src/services/textosensurado.py
import os
import re
import unicodedata
from typing import Dict, Any, List, Tuple
from src.Connection.Connection import fetch_all, Connection
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

from src.Connection.Connection import fetch_all, Connection

MODEL_PATH = os.getenv("ML_MODEL_PATH", "models/profanity_lr.joblib")


def normalizar(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto

def getgroserias() -> List[str]:
    sql = "SELECT palabra FROM groserias;"
    filas = fetch_all(sql)
    return [fila["palabra"] for fila in filas]


def getTextosensurtado(texto_original: str) -> Dict[str, Any]:
    groserias = getgroserias()
    texto_normalizado = normalizar(texto_original)

    mapa_indices = []
    j = 0
    for c in texto_original:
        normal_c = normalizar(c)
        for _ in normal_c:
            mapa_indices.append(j)
        j += 1

    mascara = [False] * len(texto_original)
    groserias_encontradas = []

    for groseria in groserias:
        palabra_norm = normalizar(groseria)
        patron = rf'\b{re.escape(palabra_norm)}\b'
        for match in re.finditer(patron, texto_normalizado):
            start, end = match.span()
            groserias_encontradas.append(groseria)
            for i in range(start, end):
                if i < len(mapa_indices):
                    original_i = mapa_indices[i]
                    mascara[original_i] = True

    texto_censurado = "".join(
        "*" if mascara[i] and c.isalnum() else c
        for i, c in enumerate(texto_original)
    )

    return {
        "Texto_censurado": texto_censurado,
        "Texto_original": texto_original,
        "Groserias": sorted(set(groserias_encontradas))
    }


def _build_pipeline() -> Pipeline:
    vectorizer = CountVectorizer(
        analyzer="char",
        ngram_range=(3, 5),
        lowercase=True,
        strip_accents="unicode"
    )
    model = LinearRegression()  # explícito: regresión lineal
    return Pipeline([
        ("vec", vectorizer),
        ("lr", model),
    ])

def add_training_sample(texto: str, label: int) -> int:
    sql = "INSERT INTO training_samples (texto, label) VALUES (%s, %s) RETURNING id;"
    conn = Connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (texto, label))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id
    finally:
        conn.close()

def _load_training_data() -> Tuple[List[str], List[int]]:
    rows = fetch_all("SELECT texto, label FROM training_samples ORDER BY id ASC;")
    X = [r["texto"] for r in rows]
    y = [int(r["label"]) for r in rows]
    return X, y

def train_linear_model() -> Dict[str, Any]:
    X, y = _load_training_data()
    if len(X) < 10:
        return {"ok": False, "msg": "Se requieren al menos 10 ejemplos en training_samples para entrenar."}

    pipe = _build_pipeline()
    pipe.fit(X, y)

    preds = pipe.predict(X)
    mse = float(mean_squared_error(y, preds))

    os.makedirs(os.path.dirname(MODEL_PATH) or ".", exist_ok=True)
    dump(pipe, MODEL_PATH)

    return {"ok": True, "mse": mse, "samples": len(X), "model_path": MODEL_PATH}

def _load_model() -> Pipeline:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Modelo no encontrado. Entrena primero con /ml/train.")
    return load(MODEL_PATH)

def predict_profanity_score(texto: str) -> Dict[str, Any]:
    pipe = _load_model()
    score = float(pipe.predict([texto])[0]) 
    is_offensive = score >= 0.5

    censurado = getTextosensurtado(texto)

    return {
        "texto": texto,
        "score_regresion": round(score, 4),
        "ofensivo_ml": bool(is_offensive),
        "censura_diccionario": censurado
    }