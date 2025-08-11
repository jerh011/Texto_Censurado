import re
import unicodedata
from src.Connection.Connection import fetch_all

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    return texto

def getgroserias():
    sql = "SELECT palabra FROM groserias;"
    filas = fetch_all(sql)
    return [fila["palabra"] for fila in filas]  

def getTextosensurtado(texto_original):
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

    # Construir texto censurado
    texto_censurado = "".join(
        "*" if mascara[i] and c.isalnum() else c
        for i, c in enumerate(texto_original)
    )

    return {
        "Texto_censurado": texto_censurado,
        "Texto_original": texto_original,
        "Groserias": sorted(set(groserias_encontradas))
    }
