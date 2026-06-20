# Urban Routes Test Automation

## Description

This project contains automated tests for the Urban Routes web application, a taxi-booking platform. The tests cover the complete order flow: setting up a route, selecting a fare, adding a phone number, adding a payment card, entering a message for the driver, requesting additional items, and confirming the order.

The goal is to validate that every step of the booking flow works correctly from end to end through Selenium-based automation.

## Test Coverage

The following scenarios are covered:

* Setting origin and destination addresses
* Selecting the Comfort fare
* Entering and confirming a phone number via SMS verification code
* Adding a credit card as a payment method
* Entering a message for the driver
* Requesting a blanket and tissues
* Requesting 2 ice creams
* Confirming the order and verifying the driver information modal appears

## Technologies and Techniques Used

* **Python 3.12** — Main programming language
* **Pytest 7.x** — Framework for organizing and executing tests
* **Selenium 4.x** — Browser automation using Chrome
* **Page Object Model (POM)** — Design pattern that separates page locators and methods from test logic
* **WebDriverWait + Expected Conditions** — Explicit waits for handling dynamic web elements
* **Chrome DevTools Protocol (CDP)** — Used to capture the SMS confirmation code from network logs

## Running the Tests

1. Install dependencies:

```bash
pip install pytest selenium
```

2. Make sure ChromeDriver is installed and compatible with your version of Google Chrome.

3. Configure the application URL in `data.py`.

> **Note:** The server URL is temporary and expires periodically. Before running the tests, replace the value of `URBAN_ROUTES_URL` with a new active URL.

4. Run the test suite:

```bash
pytest main.py
```

## Project Structure

* `main.py` → UrbanRoutesPage Page Object class and TestUrbanRoutes test cases
* `helpers.py` → `retrieve_phone_code` function for capturing the SMS verification code from network logs
* `data.py` → URLs, addresses, phone number, payment card data, and driver message
* `README.md` → Project documentation
* `.gitignore` → Files ignored by Git
