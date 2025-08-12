from difflib import get_close_matches
from core.utils import normalizar
from core.templates import header, class_open, word_block
import re

def build_code(plataforma: str, pasos: list[str], acciones: dict, sanitized_name: str,
               dni: str, usuario: str, clave: str, word_name: str) -> str:
    class_name = f"Test_{sanitized_name}"
    method_name = f"test_{sanitized_name.lower()}"
    user_block = f'''user = {{
    "dni": "{dni}",
    "usuario": "{usuario}",
    "clave": "{clave}"
    }}'''
    preamble = """        iniciar_sesion = IniciarSesion(self.driver)
        iniciar_sesion.login(user['dni'], user['usuario'], user['clave'])
        tools = Tools(self.driver)
        time.sleep(5)
"""
    code = header(plataforma, sanitized_name, user_block)
    code += class_open(class_name, method_name, preamble)

    claves_norm = {normalizar(k): k for k in acciones.keys()}

    for paso in [p for p in pasos if p.strip()]:
        # 1) esperar/descansar <N> segundos
        m_espera = re.match(r"(?:esperar|descansar)\s+(\d+)\s+segundos?", paso, re.I)
        if m_espera:
            num_segundos = m_espera.group(1)
            code += f"        time.sleep({num_segundos})\n"
            continue

        # 2) esperar/expect locador|locator <NOMBRE>
        m_wait_loc = re.match(r"(?:esperar|expect)\s+(?:locador|locator)\s+(.+)", paso, re.I)
        if m_wait_loc:
            nombre = m_wait_loc.group(1).strip().replace(" ", "_")
            code += f'        tools.expected_locator("//{nombre}")# Reemplazar con xpath real\n'  # 👈 agregar \n
            continue

        # 3) click / clickear ...
        m_click = re.match(r"(?:click|clickear)(?: en| boton)?\s+(.+)", paso, re.I)
        if m_click:
            nombre = m_click.group(1).strip().replace(" ", "_")
            code += f'        tools.click_xpath("//{nombre}")  # Reemplazar con xpath real\n'
            continue

        # 4) contains esperar locador|locator <PALABRA>
        m_wait_contains = re.match(r"contains\s+(?:esperar|expect)\s+(?:locador|locator)\s+(.+)", paso, re.I)
        if m_wait_contains:
            palabra = m_wait_contains.group(1).strip()
            # Si puede venir con comillas simples, escapalas:
            palabra = palabra.replace("'", "\\'")
            if plataforma.lower() == "android":
                # Texto visible o content-desc
                xpath = f"//*[contains(@text, '{palabra}')]"
            else:
                # iOS: name/label/value
                xpath = f"//*[contains(@label, '{palabra}')]"
            code += f'        tools.expected_locator("{xpath}")\n'
            continue

        # 5) click / clickear contains <PALABRA>
        if paso.lower().startswith(("contains click", "contains clickear")):
            # quitar el prefijo que sea
            if paso.lower().startswith("contains clickear"):
                palabra = paso[len("contains clickear"):].strip()
            else:
                palabra = paso[len("contains click"):].strip()

            attr = "text" if plataforma.lower() == "android" else "label"
            code += f'        tools.click_xpath("//*[contains(@{attr}, \'{palabra}\')]")\n'
            continue

        # 6) fallback JSON + fuzzy
        norm = normalizar(paso)
        if norm in claves_norm:
            for linea in acciones[claves_norm[norm]].splitlines():
                code += f"        {linea}\n"
        else:
            posibles = get_close_matches(norm, list(claves_norm.keys()), n=1, cutoff=0.6)
            if posibles:
                key = claves_norm[posibles[0]]
                code += f"        # ⚠️ Interpretando “{paso}” como “{key}”\n"
                for linea in acciones[key].splitlines():
                    code += f"        {linea}\n"
            else:
                code += f'        # 🔴 Acción no reconocida: "{paso}"\n'

    code += word_block(word_name, sanitized_name, dni, usuario, clave)
    return code
