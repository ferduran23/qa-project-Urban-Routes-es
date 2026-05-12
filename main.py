import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def retrieve_phone_code(driver) -> str:
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
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.CSS_SELECTOR, "button.button.round")
    comfort_rate = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    phone_field = (By.ID, "phone")
    phone_button = (By.XPATH, "//div[contains(text(),'Número de teléfono')]")
    next_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    code_field = (By.XPATH, "//input[@id='code']")
    card_button = (By.CSS_SELECTOR, ".pp-button.filled")
    add_card_button = (By.XPATH, "//div[contains(text(),'Agregar tarjeta')]")
    payment_button = (By.XPATH, "//div[contains(@class, 'pp-button') and contains(., 'Método de pago')]")
    card_number_field = (By.ID, "number")
    card_code_field = (By.CSS_SELECTOR, "input.card-input[name='code']")
    link_button = (By.XPATH, "//button[contains(text(),'Agregar')]")
    confirm_code_button = (By.XPATH, "//button[text()='Confirmar']")
    message_field = (By.ID, "comment")
    blanket_switch = (By.XPATH, "//div[text()='Manta y pañuelos']")
    ice_cream_counter = (By.XPATH, "//div[text()='Helado']/following-sibling::div//div[contains(@class,'counter-plus')]")
    search_modal = (By.XPATH, "//div[contains(text(),'Buscar automóvil')]")
    driver_modal = (By.CLASS_NAME, "order-body")
    order_button = (By.CSS_SELECTOR, "button.smart-button")

    def __init__(self, driver):
        self.driver = driver

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

    def click_call_taxi(self):
        button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.call_taxi_button)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def select_comfort_rate(self):
        comfort = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.comfort_rate)
        )
        self.driver.execute_script("arguments[0].click();", comfort)

    def set_phone_number(self, phone_number):
        phone_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.phone_button)
        )
        self.driver.execute_script("arguments[0].click();", phone_button)
        self.driver.find_element(*self.phone_field).send_keys(phone_number)
        self.driver.find_element(*self.next_button).click()

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
        self.driver.execute_script("document.querySelector('.payment-picker').remove()")

    def set_message(self, message):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.message_field)
        ).send_keys(message)

    def wait_overlay(self):
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script(
                "return Array.from(document.querySelectorAll('.overlay')).every(e => e.getBoundingClientRect().width === 0)"
            )
        )

    def order_blanket_and_tissues(self):
        self.wait_overlay()
        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.blanket_switch)
        )
        self.driver.execute_script("arguments[0].click();", element)

    def order_ice_cream(self):
        self.wait_overlay()
        for i in range(2):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ice_cream_counter)
            ).click()

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

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_complete_taxi_order(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_call_taxi()
        routes_page.select_comfort_rate()
        routes_page.set_phone_number(data.phone_number)
        code = retrieve_phone_code(self.driver)
        routes_page.set_phone_code(code)
        routes_page.add_card(data.card_number, data.card_code)
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "comment"))
        )
        routes_page.set_message(data.message_for_driver)
        routes_page.order_blanket_and_tissues()
        routes_page.order_ice_cream()
        routes_page.click_order_taxi()
        routes_page.wait_for_driver_modal()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
