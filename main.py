import data
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    # Las pruebas avanzan por el mismo pedido en este orden, compartiendo el navegador.
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)

    def test_set_route(self):
        # Inicia el flujo configurando y verificando las direcciones del viaje.
        page = UrbanRoutesPage(self.driver)
        page.open_app(data.URBAN_ROUTES_URL)
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from() == data.ADDRESS_FROM
        assert page.get_to() == data.ADDRESS_TO

    def test_select_comfort(self):
        # Abre las tarifas, elige Comfort y comprueba que quede activa.
        page = UrbanRoutesPage(self.driver)
        page.open_fare_options()
        page.select_comfort()
        assert page.get_active_plan() == 'Comfort'

    def test_add_phone(self):
        # Registra el teléfono y verifica que aparezca en la página.
        page = UrbanRoutesPage(self.driver)
        page.add_phone(data.PHONE_NUMBER)
        assert data.PHONE_NUMBER in page.get_phone()

    def test_add_card(self):
        # Agrega la tarjeta y valida que sea el método de pago seleccionado.
        page = UrbanRoutesPage(self.driver)
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert page.get_payment_method() == 'Tarjeta'

    def test_set_driver_message(self):
        # Escribe el mensaje y comprueba el valor del campo.
        page = UrbanRoutesPage(self.driver)
        page.set_driver_message(data.MESSAGE_FOR_DRIVER)
        assert page.get_driver_message() == data.MESSAGE_FOR_DRIVER

    def test_request_blanket_and_tissues(self):
        # Activa manta y pañuelos y valida el estado del switch.
        page = UrbanRoutesPage(self.driver)
        page.scroll_to_extras()
        page.click_blanket_and_handkerchiefs()
        assert page.is_blanket_and_handkerchiefs_selected()

    def test_request_two_ice_creams(self):
        # Añade dos helados y valida el contador.
        page = UrbanRoutesPage(self.driver)
        page.add_ice_cream(2)
        assert page.get_ice_cream_amount() == 2

    def test_car_search_modal_appears(self):
        # Envía la solicitud y verifica el modal devuelto por el Page Object.
        page = UrbanRoutesPage(self.driver)
        assert page.order_taxi().is_displayed()
    # Paso Extra: Verificar los datos del conductor en el modal.

    def test_driver_info_appears(self):
        # Espera desde el Page Object hasta que aparezcan los datos del conductor.
        page = UrbanRoutesPage(self.driver)
        assert page.wait_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
