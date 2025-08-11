from flask import Blueprint, jsonify, request
from src.services.textosensurado import getTextosensurtado, getgroserias

bp = Blueprint("main", __name__)

@bp.get("/")
def root():
    return jsonify({"message": "API en funcionamiento"})

@bp.get("/status")
def status():
    return jsonify(ok=True, message="API viva")

# GET con texto en la URL (admite espacios y '/')
@bp.get("/censurado/<text>")
def route_censurado_get(text: str):
    resultado = getTextosensurtado(text)
    return jsonify(resultado)

@bp.get("/groserias")
def route_groserias():
    palabras = getgroserias()  # lista de strings
    return jsonify(palabras)
