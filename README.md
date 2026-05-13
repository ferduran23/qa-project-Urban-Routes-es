# Automatización Urban Routes

## Descripción

Este proyecto contiene pruebas automatizadas para la aplicación web Urban Routes, una plataforma para solicitar taxis. Las pruebas cubren el flujo completo de un pedido: configurar una ruta, seleccionar una tarifa, agregar un número de teléfono, agregar una tarjeta de pago, escribir un mensaje al conductor, solicitar artículos adicionales y confirmar el pedido.

El objetivo es validar que todos los pasos del flujo funcionen correctamente de principio a fin mediante automatización con Selenium.

## Qué se está probando

Se cubren los siguientes escenarios:

* Configuración de la ruta de origen y destino
* Selección de la tarifa Comfort
* Ingreso y confirmación del número de teléfono con código SMS
* Agregado de tarjeta de crédito como método de pago
* Ingreso de mensaje para el conductor
* Solicitud de manta y pañuelos
* Solicitud de 2 helados
* Confirmación del pedido y aparición del modal con información del conductor

## Tecnologías y técnicas utilizadas

* **Python 3.12** — lenguaje principal del proyecto
* **Pytest 7.x** — framework para organizar y ejecutar las pruebas
* **Selenium 4.x** — automatización del navegador Chrome
* **Page Object Model (POM)** — patrón de diseño que separa los locators y métodos de la página de la lógica de los tests
* **WebDriverWait + Expected Conditions** — esperas explícitas para manejar elementos dinámicos
* **Chrome DevTools Protocol (CDP)** — usado para capturar el código de confirmación SMS desde los logs de red

## Cómo correr las pruebas

1. Instalar dependencias:
   ```
   pip install pytest selenium
   ```

2. Asegurarse de tener ChromeDriver instalado y compatible con la versión de Chrome instalada.

3. Configurar la URL de la aplicación en `data.py`. La URL del servidor es **temporal**: caduca periódicamente, por lo que debe reemplazarse por una nueva URL activa antes de correr las pruebas. La variable a actualizar es `URBAN_ROUTES_URL`.

4. Ejecutar las pruebas:
   ```
   pytest main.py
   ```

## Estructura del proyecto

* `main.py` → Clase Page Object `UrbanRoutesPage` y casos de prueba `TestUrbanRoutes`
* `helpers.py` → Función `retrieve_phone_code` para capturar el código SMS desde los logs de red
* `data.py` → URLs, direcciones, número de teléfono, datos de tarjeta y mensaje del conductor
* `README.md` → Documentación del proyecto
* `.gitignore` → Archivos ignorados por Git