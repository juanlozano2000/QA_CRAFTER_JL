def header(plataforma: str, sanitized_name: str, user_block: str) -> str:
    opt = "XCUITestOptions" if plataforma == "iOS" else "UiAutomator2Options"
    return f"""import pytest
from appium import webdriver
from appium.options.{plataforma.lower()} import {opt}
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from {plataforma.lower()}.Iniciar_Sesion import IniciarSesion
from {plataforma.lower()}.Tools import Tools, screenshot_folder

grupo_de_imagenes = ['{sanitized_name}_0', '{sanitized_name}_1', '{sanitized_name}_2']

{user_block}
"""

def header_mayorista(plataforma: str, sanitized_name: str, user_block: str) -> str:
    opt = "XCUITestOptions" if plataforma == "iOS" else "UiAutomator2Options"
    return f"""import pytest
from appium import webdriver
from appium.options.{plataforma.lower()} import {opt}
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from {plataforma.lower()}.Iniciar_Sesion import IniciarSesion_mayorista
from {plataforma.lower()}.Tools import Tools, screenshot_folder

grupo_de_imagenes = ['{sanitized_name}_0', '{sanitized_name}_1', '{sanitized_name}_2']

{user_block}
"""

def class_open(class_name: str, method_name: str, preamble_block: str) -> str:
    return f"""
@pytest.mark.usefixtures('setWebdriver')
class {class_name}:

    def {method_name}(self):
{preamble_block}        # Aqui comienza el test
"""

def word_block(word_name: str, sanitized_name: str, dni: str, usuario: str, clave: str) -> str:
    return f"""
        # CREACION DEL DOCUMENTO WORD
        resized_images = []
        for image_name in grupo_de_imagenes:
            tools.achicarImgs(image_name)
            resized_images.append(f"{{image_name}}_r")
        time.sleep(5)
        tools.create_word_with_selected_images("{word_name}.docx", resized_images, f"{dni}, {usuario}, {clave}")
"""
def word_block_mayorista(word_name: str, sanitized_name: str, usuario: str, clave: str) -> str:
    return f"""
        # CREACION DEL DOCUMENTO WORD
        resized_images = []
        for image_name in grupo_de_imagenes:
            tools.achicarImgs(image_name)
            resized_images.append(f"{{image_name}}_r")
        time.sleep(5)
        tools.create_word_with_selected_images("{word_name}.docx", resized_images, f"{usuario}, {clave}")
"""