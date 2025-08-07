from ios.Tools import Tools
from selenium.common.exceptions import NoSuchElementException
import time

class IniciarSesion:
    def __init__(self, driver):
        self.driver = driver
        self.tools = Tools(driver)

    def first_notification_alert(self):
        try:
            self.tools.click_xpath("//XCUIElementTypeButton[@name='Allow']")   
        except NoSuchElementException:
            print('No se encontro el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def second_alert(self):
        try:
            self.tools.click_xpath('//XCUIElementTypeButton[@name="Allow"]')
        except NoSuchElementException:
            print('No se encontro el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def website_alert(self):
        try:
            self.tools.click_xpath('//XCUIElementTypeButton[@name="Allow"]')
        except NoSuchElementException:
            print('No se encontro el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def contacts_alert(self):
        try:
            self.tools.click_xpath("//XCUIElementTypeButton[@name='Don’t Allow']")
        except NoSuchElementException:
            print('No se encontro el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def circle_balls_1(self):
        self.tools.click_className('XCUIElementTypePageIndicator')
    def circle_balls_2(self):
        self.tools.click_className('XCUIElementTypePageIndicator')

    def circle_balls_3(self):
        self.tools.scroll_carrousel('Izquierda')

    def location_alert(self):
        try:
            self.tools.click_ACCESSIBILITY_ID("Allow While Using App")
            time.sleep(5)
        except NoSuchElementException:
            print('No se encontró el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def btn_click_empezar(self):
        self.tools.click_xpath("/XCUIElementTypeApplication/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeScrollView/XCUIElementTypeOther/XCUIElementTypeOther[4]/XCUIElementTypeButton/XCUIElementTypeStaticText")

    def btn_cancelar(self):
        self.tools.click_xpath('//XCUIElementTypeButton[@name="Cancelar"]')

    def btn_ambiente(self):
        self.tools.click_xpath('//XCUIElementTypeButton[@name="DESA"]')

    def btn_ambiente_homo(self):
        self.tools.click_xpath("/XCUIElementTypeApplication/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeOther[3]/XCUIElementTypeStaticText[1]")

    def btn_ambiente_homo_balanceador(self):
        self.tools.click_xpath("/XCUIElementTypeApplication/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeStaticText")
        time.sleep(5)

    def btn_yaSoyGalicia(self):
        self.tools.click_xpath('//XCUIElementTypeButton[@name="Ya soy Galicia"]')

    def input_dni(self, dni):
        self.tools.set_id("/XCUIElementTypeApplication/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeTextField", dni)

    def input_user(self, user):
        self.tools.set_id("/XCUIElementTypeApplication/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeSecureTextField[1]", user)

    def input_clave(self, clave):
        self.tools.set_id("/XCUIElementTypeApplication/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeSecureTextField[2]", clave)

    def ingresar_login(self):
        self.tools.click_ACCESSIBILITY_ID("Ingresar")
        time.sleep(12)

    def cerrar_tyc(self):
        try:
            self.tools.click_xpath_login('//XCUIElementTypeButton[@name="circle close"]')
            time.sleep(3)
            self.tools.click_xpath_login('//XCUIElementTypeButton[@name="Sí, más tarde"]')
        except NoSuchElementException:
            print('No se encontro terminos y condiciones')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def cerrar_token(self):
        try:
            self.tools.click_xpath_login('//XCUIElementTypeButton[@name="ic close"]')
            time.sleep(5)
            #self.tools.click_position(400,69)
            #self.tools.click_position(214,650)
            #self.tools.click_position(194,262)
            time.sleep(5)
        except NoSuchElementException:
            print('No se encontro el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        
    
    def cerrar_modal(self):
        self.tools.click_xpath('//XCUIElementTypeButton[@name="Cerrar"]')
        time.sleep(5)

    def cerrar_modal_listo(self):
        try:
            self.tools.click_xpath_login('//*[contains(@label, "Listo")]')
        except NoSuchElementException:
            print('No se encontro el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def  cerrar_sesion(self):
        self.tools.click_xpath('//XCUIElementTypeButton[@name="Más"]')
        self.tools.scroll(208,770, 208, 235)
        self.tools.click_xpath('//XCUIElementTypeStaticText[@name="Cerrar sesión"]')
        self.tools.click_xpath('//XCUIElementTypeButton[@name="Aceptar"]')

    def loguearse_sin_alerts(self, dni, user, clave):
        self.input_dni(dni)
        self.input_user(user)
        self.input_clave(clave)
        self.ingresar_login()
        self.cerrar_tyc()
        self.cerrar_token()
    
    def cerrarModalEntrada(self):
        try:
            self.tools.click_xpath_login('//XCUIElementTypeButton[@name="Omitir"]')
            time.sleep(5)
        except NoSuchElementException:
            print('No se encontro el activar token')
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

        


    def login(self, dni, user, clave):
        #time.sleep(15)
        time.sleep(3)
        self.circle_balls_1()
        self.circle_balls_2()
        self.circle_balls_3()
        self.btn_click_empezar()
        self.btn_ambiente()
        self.btn_ambiente_homo()
        self.btn_ambiente_homo_balanceador()
        time.sleep(4)
        self.first_notification_alert()
        self.location_alert()
        self.btn_yaSoyGalicia()
        self.input_dni(dni)
        self.input_user(user)
        self.input_clave(clave)
        self.ingresar_login()
        self.second_alert()
        self.contacts_alert()
        time.sleep(5)
        self.cerrar_tyc()
        self.cerrar_token()
        self.cerrar_modal_listo()
        self.cerrarModalEntrada()
