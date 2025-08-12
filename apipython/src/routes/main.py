from flask import Blueprint, jsonify
from src.services.textosensurado import getTextosensurtado, getgroserias

bp = Blueprint("main", __name__)

@bp.get("/")
def root():
    return jsonify({"message": "API en funcionamiento"})

@bp.get("/censurado/<path:text>")
def route_censurado_get(text: str):
    resultado = getTextosensurtado(text)

    if not resultado or not resultado.get("Groserias"):
        return jsonify({
            "Groserias": [],
            "Texto_censurado": "",
            "Texto_original": text
        })

    return jsonify(resultado)


@bp.get("/groserias")
def route_groserias():
    return jsonify(getgroserias())
