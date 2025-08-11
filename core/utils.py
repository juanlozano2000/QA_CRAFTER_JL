# Archivo para alojar funciones generales de la app

import json, unicodedata
import streamlit as st

@st.cache_data
def cargar_acciones(ruta: str):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def normalizar(texto: str) -> str:
    t = texto.lower().strip()
    t = unicodedata.normalize("NFD", t)
    return ''.join(c for c in t if unicodedata.category(c) != 'Mn')
