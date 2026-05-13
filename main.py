import data
from helpers import retrieve_phone_code
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.CSS_SELECTOR, "button.button.round")

    comfort_rate_card = (By.XPATH, "//div[contains(@class,'tcard') and .//div[@class='tcard-title' and text()='Comfort']]")
    comfort_rate_title = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")

    phone_field = (By.ID, "phone")
    phone_button = (By.XPATH, "//div[contains(text(),'Número de teléfono')]")
    next_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    code_field = (By.XPATH, "//input[@id='code']")

    payment_button = (By.XPATH, "//div[contains(@class, 'pp-button') and contains(., 'Método de pago')]")
    add_card_button = (By.XPATH, "//div[contains(text(),'Agregar tarjeta')]")
    card_number_field = (By.ID, "number")
    card_code_field = (By.CSS_SELECTOR, "input.card-input[name='code']")
    link_button = (By.XPATH, "//button[contains(text(),'Agregar')]")
    close_payment_modal_button = (By.XPATH, "//div[contains(@class,'payment-picker') and contains(@class,'open')]//button[contains(@class,'close-button')]")

    confirm_code_button = (By.XPATH, "//button[text()='Confirmar']")
    message_field = (By.ID, "comment")

    blanket_switch_input = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div//input[@class='switch-input']")
    blanket_switch_clickable = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div//span[@class='slider round']")

    ice_cream_counter = (By.XPATH, "//div[text()='Helado']/following-sibling::div//div[contains(@class,'counter-plus')]")
    ice_cream_value = (By.XPATH, "//div[text()='Helado']/following-sibling::div//div[contains(@class,'counter-value')]")

    order_button = (By.CSS_SELECTOR, "button.smart-button")
    driver_modal = (By.CLASS_NAME, "order-body")

    def __init__(self, driver):
        self.driver = driver

    # ── Ruta ──────────────────────────────────────────────────────────────────

    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    # ── Taxi ──────────────────────────────────────────────────────────────────

    def click_call_taxi(self):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.call_taxi_button)
        ).click()

    def select_comfort_rate(self):
        WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.comfort_rate_title)
        ).click()

    def get_comfort_rate_card(self):
        return WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.comfort_rate_card)
        )

    # ── Teléfono ──────────────────────────────────────────────────────────────

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.phone_button)
        ).click()
        self.driver.find_element(*self.phone_field).send_keys(phone_number)
        self.driver.find_element(*self.next_button).click()

    def get_phone(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def set_phone_code(self, code):
        code_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.code_field)
        )
        code_input.send_keys(code)
        self.driver.find_element(*self.confirm_code_button).click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.code_field)
        )
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'modal')]"))
        )

    # ── Tarjeta ───────────────────────────────────────────────────────────────

    def add_card(self, card_number, card_code):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.payment_button)
        ).click()
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.add_card_button)
        ).click()
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "overlay"))
        )
        number = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.card_number_field)
        )
        number.clear()
        number.send_keys(card_number)
        cvv = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.card_code_field)
        )
        cvv.clear()
        cvv.send_keys(card_code)
        cvv.send_keys(Keys.TAB)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.link_button)
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.close_payment_modal_button)
        ).click()

    def get_current_payment_method(self):
        return self.driver.find_element(*self.payment_button).text

    # ── Mensaje ───────────────────────────────────────────────────────────────

    def set_message(self, message):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.message_field)
        ).send_keys(message)

    def get_message(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    # ── Manta y pañuelos ──────────────────────────────────────────────────────

    def _wait_overlay_gone(self):
        WebDriverWait(self.driver, 20).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "overlay"))
        )

    def order_blanket_and_tissues(self):
        self._wait_overlay_gone()
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.blanket_switch_clickable)
            )
            self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            # Fallback: clic directo sobre el input checkbox vía JS
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.blanket_switch_input)
            )
            self.driver.execute_script("arguments[0].click();", element)

    def is_blanket_checked(self):
        switch = self.driver.find_element(*self.blanket_switch_input)
        return switch.get_property('checked')

    # ── Helados ───────────────────────────────────────────────────────────────

    def order_ice_cream(self, amount=2):
        self._wait_overlay_gone()
        for _ in range(amount):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ice_cream_counter)
            ).click()

    def get_amount_of_ice_cream(self):
        value = self.driver.find_element(*self.ice_cream_value).text
        return int(value)

    # ── Pedido ────────────────────────────────────────────────────────────────

    def click_order_taxi(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.order_button)
        ).click()

    def wait_for_driver_modal(self):
        WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located(self.driver_modal)
        )


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=options)
        try:
            cls.driver.get(data.URBAN_ROUTES_URL)

            cls.routes_page = UrbanRoutesPage(cls.driver)
            cls.routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
            cls.routes_page.click_call_taxi()
            cls.routes_page.select_comfort_rate()
            cls.routes_page.set_phone_number(data.PHONE_NUMBER)
            code = retrieve_phone_code(cls.driver)
            cls.routes_page.set_phone_code(code)
            cls.routes_page.add_card(data.CARD_NUMBER, data.CARD_CODE)
            WebDriverWait(cls.driver, 20).until(
                EC.element_to_be_clickable((By.ID, "comment"))
            )
            cls.routes_page.set_message(data.MESSAGE_FOR_DRIVER)
            cls.routes_page.order_blanket_and_tissues()
            cls.routes_page.order_ice_cream(2)
        except Exception:
            cls.driver.quit()
            raise

    # ── Tests ──────────────────────────────────────────────────────────────────

    def test_set_route(self):
        assert self.routes_page.get_from() == data.ADDRESS_FROM
        assert self.routes_page.get_to() == data.ADDRESS_TO

    def test_select_comfort_rate(self):
        card = self.routes_page.get_comfort_rate_card()
        assert 'active' in card.get_attribute('class')

    def test_fill_phone_number(self):
        assert self.routes_page.get_phone() == data.PHONE_NUMBER

    def test_fill_card(self):
        assert 'Tarjeta' in self.routes_page.get_current_payment_method()

    def test_comment_for_driver(self):
        assert self.routes_page.get_message() == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        assert self.routes_page.is_blanket_checked() is True

    def test_order_2_ice_creams(self):
        assert self.routes_page.get_amount_of_ice_cream() == 2

    def test_car_search_modal_appears(self):
        self.routes_page.click_order_taxi()
        self.routes_page.wait_for_driver_modal()
        assert self.driver.find_element(*self.routes_page.driver_modal).is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
