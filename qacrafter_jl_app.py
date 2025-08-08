import streamlit as st
import json
import os
import unicodedata
from difflib import get_close_matches
from io import StringIO
import streamlit.components.v1 as components
import re


# --------- CONFIGURACIÓN DE PÁGINA ---------
st.set_page_config(page_title="QA Crafter JL", page_icon="🛠️")
st.title("🛠️ QA Crafter JL")
st.markdown("### _Generador AI de scripts automatizados para Android e iOS_")
st.markdown("Versión 1.2 · by **Juan Ignacio Lozano - L1006036**")
st.markdown("---")

# --------- INPUTS DINÁMICOS ---------
plataforma = st.selectbox(
    "📱 Seleccione tecnología:",
    ["Android", "iOS"]
)

test_class_name_raw = st.text_input(
    "📝 Nombre de la clase de test:",
    "Nombre del Test"
)
# eliminar espacios de cualquier parte del nombre
sanitized_name = "_".join(test_class_name_raw.split())

st.markdown("#### 🔐 Credenciales de usuario")
dni = st.text_input("DNI", "Numero_dni")
usuario = st.text_input("Usuario", "usuario01")
clave = st.text_input("Clave", "1003")

word_name = st.text_input(
    "📚 Nombre del documento word:",
    f"{sanitized_name}"
)

# --------- CACHÉ PARA CARGA DE ACCIONES ---------
@st.cache_data
def cargar_acciones(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

json_path = os.path.join("actions", f"{plataforma.lower()}.json")
try:
    acciones = cargar_acciones(json_path)
except FileNotFoundError:
    st.error(f"No se encontró el archivo de acciones para {plataforma}")
    st.stop()

# --------- ÁREA DE INSTRUCCIONES ---------
st.markdown("✍️ Escribí los pasos del test, uno por línea:")
st.markdown("""**_Ejemplo:_**
- _click en tarjetas_  
- _scrollear carrousel a la izq_  
- _click en boton pausar_""")
entrada = st.text_area("Instrucciones:", height=200)

# --------- FUNCIONES AUXILIARES ---------
def normalizar(texto: str) -> str:
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

# --------- GENERACIÓN DE CÓDIGO ---------
if st.button("✨ Generar Código"):
    if not entrada.strip():
        st.warning("Por favor ingresa al menos un paso en el área de instrucciones.")
    else:
        pasos = [p for p in entrada.split("\n") if p.strip()]
        class_name = f"Test_{sanitized_name}"
        method_name = f"test_{sanitized_name.lower()}"
        codigo = f"""import pytest
from appium import webdriver
from appium.options.{plataforma.lower()} import {'XCUITestOptions' if plataforma=='iOS' else 'UiAutomator2Options'}
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from {plataforma.lower()}.Iniciar_Sesion import IniciarSesion
from {plataforma.lower()}.Tools import Tools, screenshot_folder

grupo_de_imagenes = ['{sanitized_name}_0', '{sanitized_name}_1', '{sanitized_name}_2']

user = {{
    "dni": "{dni}",
    "usuario": "{usuario}",
    "clave": "{clave}"
}}

@pytest.mark.usefixtures('setWebdriver')
class {class_name}:

    def {method_name}(self):
        iniciar_sesion = IniciarSesion(self.driver)
        iniciar_sesion.login(user['dni'], user['usuario'], user['clave'])
        tools = Tools(self.driver)
        time.sleep(5)

        #Aqui comienza el test
"""
        claves_norm = {normalizar(k): k for k in acciones.keys()}
        for paso in pasos:
            # 1) Handler dinámico para variantes de “click”
            m = re.match(r"(?:click|clickear)(?: en| boton)?\s+(.+)", paso, re.I)
            if m:
                # Extrae la parte después de “click…”
                nombre = m.group(1).strip().replace(" ", "_")
                codigo += (
                    f'        tools.click_xpath("//{nombre}")'
                    f'  # Reemplazar con xpath real"\n'
                )
                continue

            # 2) Matching contra JSON + fuzzy match
            norm = normalizar(paso)
            if norm in claves_norm:
                bloque = acciones[claves_norm[norm]]
                for linea in bloque.splitlines():
                    codigo += f"        {linea}\n"
            else:
                posibles = get_close_matches(norm, list(claves_norm.keys()), n=1, cutoff=0.6)
                if posibles:
                    key = claves_norm[posibles[0]]
                    bloque = acciones[key]
                    codigo += f"        # ⚠️ Interpretando “{paso}” como “{key}”\n"
                    for linea in bloque.splitlines():
                        codigo += f"        {linea}\n"
                else:
                    codigo += f"        # 🔴 Acción no reconocida: \"{paso}\"\n"

            # Al final del for, cuando quieras agregar el bloque fijo:
        codigo += (
            '\n        '
            '        # CREACION DEL DOCUMENTO WORD\n'
            '        # Redimensionar imágenes\n'
            '        resized_images = []  # Lista para los nombres redimensionados\n'
            '        for image_name in grupo_de_imagenes:\n'
            '            tools.achicarImgs(image_name)\n'
            '            resized_images.append(f"{image_name}_r")  # Agregar nombre redimensionado\n'
            '        time.sleep(5)\n'
            f'        tools.create_word_with_selected_images("{word_name}.docx", resized_images, f"{dni}, {usuario}, {clave}")\n'
        )


        # Mostrar y ofrecer descarga y copiar
        st.success(f"✅ Código generado para {plataforma}")
        st.code(codigo, language="python")

        # Botón copiar con JS
        components.html(f'''
<button id="copy-btn">📋 Copiar código</button>
<script>
const code = {json.dumps(codigo)};
document.getElementById("copy-btn").addEventListener("click", () => {{
    navigator.clipboard.writeText(code);
}});
</script>
''', height=50)

        buffer = StringIO()
        buffer.write(codigo)
        st.download_button(
            label="📥 Descargar script",
            data=buffer.getvalue(),
            file_name=f"test_{plataforma.lower()}.py",
            mime="text/x-python"
        )



