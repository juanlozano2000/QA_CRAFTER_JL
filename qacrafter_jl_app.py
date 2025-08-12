import os, json
import streamlit as st
from io import StringIO
from core.utils import cargar_acciones
import streamlit.components.v1 as components
from generators.minorista import build_code as build_minorista
from generators.mayorista import build_code as build_mayorista

# --------- CONFIGURACIÓN DE PÁGINA ---------
st.set_page_config(page_title="QA Crafter JL", page_icon="🛠️")
st.title("🛠️ QA Crafter JL")
st.markdown("### _Generador AI de scripts automatizados para Android e iOS_")
st.markdown("Versión 1.2 · by **Juan Ignacio Lozano - L1006036**")
st.markdown("---")

# ----- UI -----
plataforma = st.selectbox("📱 Seleccione tecnología:", ["Android", "iOS"])
type_app = st.selectbox("Seleccione tipo de aplicación:", ["App Minorista", "App Mayorista"])

test_class_name_raw = st.text_input("📝 Nombre de la clase de test:", "Nombre del Test")
sanitized_name = "_".join(test_class_name_raw.split())

# Credenciales solo si Minorista
if type_app == "App Minorista":
    st.markdown("#### 🔐 Credenciales de usuario")
    dni = st.text_input("DNI", "Numero_dni")
    usuario = st.text_input("Usuario", "usuario01")
    clave = st.text_input("Clave", "1003")
else:
    st.markdown("#### 🔐 Credenciales de usuario (Mayorista)")
    dni = ""  # No se pide DNI
    usuario = st.text_input("Usuario", "usuario01")
    clave = st.text_input("Clave", "1003")

st.markdown("#### 📚 Nombre del documento Word")
word_name = st.text_input("Nombre del documento:", f"{sanitized_name}")

# --------- ÁREA DE INSTRUCCIONES ---------
st.markdown("✍️ Escribí los pasos del test, uno por línea:")
st.markdown("""**_Ejemplo:_**
- _click en tarjetas_  
- _scrollear carrousel a la izq_  
- _tomar foto_  
- _contains click_  
- _contains esperar locador boton pausar_  
- _esperar 3 segundos_""")
entrada = st.text_area("Instrucciones:", height=200)

# ----- Datos acciones -----
json_path = os.path.join("actions", f"{plataforma.lower()}.json")
try:
    acciones = cargar_acciones(json_path)
except FileNotFoundError:
    st.error(f"No se encontró el archivo de acciones para {plataforma}")
    st.stop()

# ----- Generación -----
if st.button("✨ Generar Código"):
    if not entrada.strip():
        st.warning("Por favor ingresa al menos un paso en el área de instrucciones.")
    else:
        pasos = [p for p in entrada.split("\n") if p.strip()]

        # ⚠️ Respetar la firma de cada builder:
        # minorista.build_code(plataforma, pasos, acciones, sanitized_name, dni, usuario, clave, word_name)
        # mayorista.build_code(plataforma, pasos, acciones, sanitized_name, word_name=None)
        if type_app == "App Minorista":
            codigo = build_minorista(
                plataforma, pasos, acciones, sanitized_name,
                dni, usuario, clave, word_name
            )
        else:
            codigo = build_mayorista(
                plataforma, pasos, acciones, sanitized_name, word_name
            )

        # ✅ Mostrar una sola vez
        st.success(f"✅ Código generado para {plataforma} - {type_app}")
        st.code(codigo, language="python")

        # ✅ Botón copiar (una sola vez)
        components.html(f'''
<button id="copy-btn">📋 Copiar código</button>
<script>
const code = {json.dumps(codigo)};
document.getElementById("copy-btn").addEventListener("click", () => {{
    navigator.clipboard.writeText(code);
}});
</script>
''', height=50)

        # ✅ Descargar (una sola vez)
        buffer = StringIO()
        buffer.write(codigo)
        st.download_button(
            label="📥 Descargar script",
            data=buffer.getvalue(),
            file_name=f"test_{plataforma.lower()}_{'minorista' if type_app=='App Minorista' else 'mayorista'}.py",
            mime="text/x-python"
        )

