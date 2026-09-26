from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    """Reúne los localizadores y acciones para interactuar con Urban Routes."""

    # Campos de origen y destino del viaje.
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        field = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.from_field))
        field.send_keys(from_address)

    def set_to(self, to_address):
        field = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.to_field))
        field.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_active_plan(self):
        return self.wait(self.active_plan).text.strip()

    def get_phone(self):
        return self.wait(self.phone_text).text.strip()

    def get_payment_method(self):
        return self.wait(self.payment_method_text).text.strip()

    def get_driver_message(self):
        return self.wait(self.driver_message).get_property('value')

    def is_blanket_and_handkerchiefs_selected(self):
        return self.wait(self.blanket_tissues_input).is_selected()

    def get_ice_cream_amount(self):
        counter = self.driver.find_elements(*self.ice_cream_counter)[0]
        return int(counter.text.strip())

    # Localizadores de tarifa, teléfono y confirmación por SMS.
    request_fares_button = (
        By.XPATH, "//button[normalize-space(.)='Pedir un taxi']")
    comfort_tariff = (By.XPATH, "//*[normalize-space(text())='Comfort']")
    active_plan = (
        By.XPATH, "//div[contains(@class,'tcard') and contains(@class,'active')]//div[@class='tcard-title']")
    phone_number_field = (
        By.XPATH, "//*[contains(concat(' ', normalize-space(@class), ' '), ' np-text ') and normalize-space(.)='Número de teléfono']")
    phone_field = (By.ID, 'phone')
    phone_text = (By.CLASS_NAME, 'np-text')
    phone_next = (By.XPATH, "//button[text()='Siguiente']")
    phone_code = (By.ID, 'code')
    phone_confirm = (
        By.XPATH, "//button[contains(.,'Confirmar') or contains(.,'Confirm')]")
    # Localizadores para abrir el método de pago y registrar una tarjeta.
    payment_button = (By.CLASS_NAME, 'pp-button')
    add_card_button = (
        By.XPATH, "//div[contains(concat(' ', normalize-space(@class), ' '), ' pp-row ')][.//div[contains(concat(' ', normalize-space(@class), ' '), ' pp-title ') and normalize-space(.)='Agregar tarjeta']]")
    payment_method_text = (By.CLASS_NAME, 'pp-value-text')
    card_number = (By.CSS_SELECTOR, "input#number.card-input")
    card_code = (By.CSS_SELECTOR, "input#code.card-input")
    card_add_button = (By.XPATH, "//button[text()='Agregar']")
    payment_close_button = (By.CSS_SELECTOR, "button.close-button.section-close")
    # Mensaje y extras opcionales del pedido.
    driver_message = (By.ID, 'comment')
    blanket_tissues_input = (
        By.XPATH, "//*[normalize-space(.)='Manta y pañuelos']/ancestor::*[.//input[contains(@class,'switch-input')]][1]//input[contains(@class,'switch-input')]")
    blanket_tissues_slider = (
        By.XPATH, "//*[normalize-space(.)='Manta y pañuelos']/ancestor::*[.//input[contains(@class,'switch-input')]][1]//span[contains(concat(' ', normalize-space(@class), ' '), ' slider ')]")
    ice_cream_plus = (
        By.XPATH, "//*[normalize-space(.)='Helado']/ancestor::*[.//div[contains(@class,'counter-plus')]][1]//div[contains(@class,'counter-plus') and normalize-space(.)='+' ]")
    ice_cream_counter = (By.CLASS_NAME, 'counter-value')
    # Elementos que indican que el pedido está en búsqueda y que ya hay conductor.
    order_button = (By.CLASS_NAME, 'smart-button')
    search_modal = (
        By.XPATH, "//*[contains(normalize-space(.),'Buscar automóvil') or contains(normalize-space(.),'Buscar un taxi')]")
    driver_info = (By.CSS_SELECTOR, "div.order-button")
    driver_rating = (By.CSS_SELECTOR, "div.order-button .order-btn-rating")

    def wait(self, locator, timeout=30):
        # Espera a que el elemento exista en el DOM antes de usarlo.
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=30):
        # Desplaza el elemento a la vista y hace clic cuando está habilitado.
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)).click()

    def open_app(self, url):
        # Abre la aplicación y espera a que carguen los campos de dirección.
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(lambda driver: driver.execute_script(
            "return document.readyState") == "complete")
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.from_field))
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.to_field))

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def open_fare_options(self):
        self.click(self.request_fares_button)

    def select_comfort(self):
        self.click(self.comfort_tariff)

    def add_phone(self, phone_number):
        # Abre el formulario, captura el código SMS y confirma el teléfono.
        self.click(self.phone_number_field)
        self.wait(self.phone_field).send_keys(phone_number)
        self.click(self.phone_next)
        self.wait(self.phone_code).send_keys(retrieve_phone_code(self.driver))
        self.click(self.phone_confirm)

    def close_payment_window(self):
        # Localiza el botón de cierre activo y espera a que desaparezca el modal.
        def visible_close_button(driver):
            buttons = [
                button for button in driver.find_elements(*self.payment_close_button)
                if button.is_displayed() and button.is_enabled()
            ]
            return buttons[-1] if buttons else False

        close_button = WebDriverWait(self.driver, 30).until(visible_close_button)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", close_button)
        close_button.click()
        WebDriverWait(self.driver, 15).until(EC.any_of(
            EC.staleness_of(close_button), EC.invisibility_of_element(close_button)))

    def add_card(self, number, code):
        # TAB quita el foco del CVV y permite que se habilite el botón Agregar.
        self.click(self.payment_button)
        self.click(self.add_card_button)
        self.wait(self.card_number).send_keys(number)
        field = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.card_code))
        field.click()
        field.clear()
        field.send_keys(code)
        field.send_keys(Keys.TAB)
        self.click(self.card_add_button)
        self.close_payment_window()

    def set_driver_message(self, message):
        self.wait(self.driver_message).send_keys(message)

    def scroll_to_extras(self):
        # Desplaza el panel para que los controles de extras queden visibles.
        slider = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.blanket_tissues_slider))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", slider)

    def click_blanket_and_handkerchiefs(self):
        # Evita cambiar el switch si ya estaba activado.
        if not self.is_blanket_and_handkerchiefs_selected():
            self.click(self.blanket_tissues_slider)

    def add_ice_cream(self, amount):
        # Incrementa el contador la cantidad de veces solicitada.
        for _ in range(amount):
            self.click(self.ice_cream_plus)

    def order_taxi(self):
        # Envía el pedido y devuelve el modal cuando ya está visible.
        self.click(self.order_button)
        return WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.search_modal))

    def wait_driver_info(self, timeout=180):
        # Espera la asignación del conductor y devuelve su calificación visible.
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.driver_info))
        rating = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.driver_rating))
        return rating.text.strip()
