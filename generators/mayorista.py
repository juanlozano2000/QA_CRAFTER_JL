from difflib import get_close_matches
from core.utils import normalizar
from core.templates import header_mayorista, class_open, word_block_mayorista
import re

def build_code(plataforma: str, pasos: list[str], acciones: dict, sanitized_name: str, usuario: str, clave: str, word_name: str | None = None) -> str:
    class_name = f"Test_{sanitized_name}"
    method_name = f"test_{sanitized_name.lower()}"
    user_block = f'''user = {{
    "usuario": "{usuario}",
    "clave": "{clave}"
    }}'''
    preamble = """        iniciar_sesion = IniciarSesion_mayorista(self.driver)
        iniciar_sesion.login(user['usuario'], user['clave'])
        tools = Tools(self.driver)
        time.sleep(5)
"""
    code = header_mayorista(plataforma, sanitized_name, user_block)
    code += class_open(class_name, method_name, preamble)

    claves_norm = {normalizar(k): k for k in acciones.keys()}

    for paso in [p for p in pasos if p.strip()]:
        # ✅ Usar \s+ (no \\s+)
        m = re.match(r"(?:click|clickear)(?: en| boton)?\s+(.+)", paso, re.I)
        if m:
            nombre = m.group(1).strip().replace(" ", "_")
            code += f'        tools.click_xpath("//{nombre}")  # Reemplazar con xpath real\n'
            continue

        #esperar o descansar
        m_espera = re.match(r"(?:esperar|descansar)\s+(\d+)\s+segundos?", paso, re.I)
        if m_espera:
            num_segundos = m_espera.group(1)
            code += f"        time.sleep({num_segundos})\n"
            continue

        norm = normalizar(paso)
        if norm in claves_norm:
            for linea in acciones[claves_norm[norm]].splitlines():
                code += f"        {linea}\n"  # ✅
        else:
            posibles = get_close_matches(norm, list(claves_norm.keys()), n=1, cutoff=0.6)
            if posibles:
                key = claves_norm[posibles[0]]
                code += f"        # ⚠️ Interpretando “{paso}” como “{key}”\n"  # ✅
                for linea in acciones[key].splitlines():
                    code += f"        {linea}\n"  # ✅
            else:
                code += f'        # 🔴 Acción no reconocida: "{paso}"\n'  # ✅

    code += word_block_mayorista(word_name, sanitized_name, usuario, clave)

    return code
