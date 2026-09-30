import data
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    def setup_method(self):
        # Cada prueba obtiene una sesión limpia de Chrome y abre la aplicación.
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=options)
        self.page = UrbanRoutesPage(self.driver)
        self.page.open_app(data.URBAN_ROUTES_URL)

    def teardown_method(self):
        # Cierra el navegador de esta prueba, incluso si una aserción falla.
        if hasattr(self, 'driver'):
            self.driver.quit()

    def _prepare_route(self):
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

    def _prepare_comfort(self):
        self._prepare_route()
        self.page.open_fare_options()
        self.page.select_comfort()

    def _prepare_phone(self):
        self._prepare_comfort()
        self.page.add_phone(data.PHONE_NUMBER)

    def _prepare_full_order(self):
        # Completa los pasos previos requeridos antes de solicitar el taxi.
        self._prepare_phone()
        self.page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        self.page.set_driver_message(data.MESSAGE_FOR_DRIVER)
        self.page.scroll_to_extras()
        self.page.click_blanket_and_handkerchiefs()
        self.page.add_ice_cream(2)

    def test_set_route(self):
        self._prepare_route()
        assert self.page.get_from() == data.ADDRESS_FROM
        assert self.page.get_to() == data.ADDRESS_TO

    def test_select_comfort(self):
        self._prepare_comfort()
        assert self.page.get_active_plan() == 'Comfort'

    def test_add_phone(self):
        self._prepare_phone()
        assert data.PHONE_NUMBER in self.page.get_phone()

    def test_add_card(self):
        self._prepare_phone()
        self.page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.get_payment_method() == 'Tarjeta'

    def test_set_driver_message(self):
        self._prepare_comfort()
        self.page.set_driver_message(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_driver_message() == data.MESSAGE_FOR_DRIVER

    def test_request_blanket_and_tissues(self):
        self._prepare_comfort()
        self.page.scroll_to_extras()
        self.page.click_blanket_and_handkerchiefs()
        assert self.page.is_blanket_and_handkerchiefs_selected()

    def test_request_two_ice_creams(self):
        self._prepare_comfort()
        self.page.scroll_to_extras()
        self.page.add_ice_cream(2)
        assert self.page.get_ice_cream_amount() == 2

    def test_car_search_modal_appears(self):
        self._prepare_full_order()
        assert self.page.order_taxi().is_displayed()

    def test_driver_info_appears(self):
        self._prepare_full_order()
        self.page.order_taxi()
        assert self.page.wait_driver_info()
