from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
from PIL import ImageGrab
import os
import time

# Rutas para las capturas de pantalla
SCREENSHOT_PATH = os.path.join(os.getcwd(), "ventas_screenshot_before.png")
SCREENSHOT_PATH2 = os.path.join(os.getcwd(), "ventas_screenshot_after.png")

# Inicia el navegador y abre la aplicación
@given('la aplicación de ventas está abierta')
def step_given_application_is_open(context):
    context.driver = webdriver.Chrome()
    context.driver.get('E:/Documentos Personales/Descargas/02_UC002/app/Ventas/index.html') 
    time.sleep(1)
    screenshot = ImageGrab.grab()
    screenshot.save(SCREENSHOT_PATH)

@when('selecciono "{value}" en el campo "producto"')
def step_when_select_product(context, value):
    select = context.driver.find_element(By.ID, "producto")
    for option in select.find_elements(By.TAG_NAME, 'option'):
        if option.text == value:
            option.click()
            break

@when('ingreso "{value}" en el campo "{field_id}"')
def step_when_input_value(context, value, field_id):
    field = context.driver.find_element(By.ID, field_id)
    field.clear()
    field.send_keys(value)

@when('hago clic en "Gestionar Venta"')
def step_when_click_gestionar_venta(context):
    button = context.driver.find_element(By.ID, 'gestionar-venta')
    button.click()
    time.sleep(1)
    screenshot = ImageGrab.grab()
    screenshot.save(SCREENSHOT_PATH2)

@then('debería ver un mensaje de éxito indicando que la venta se gestionó correctamente')
def step_then_should_see_success_message(context):
    alert = WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    actual_message = alert.text
    if "Venta gestionada exitosamente" not in actual_message:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert "Venta gestionada exitosamente" in actual_message
    alert.accept()

@then('debería ver un mensaje de error indicando que se debe seleccionar un producto')
def step_then_should_see_select_product_error(context):
    alert = WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    actual_message = alert.text
    if "Debe seleccionar un producto" not in actual_message:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert "Debe seleccionar un producto" in actual_message
    alert.accept()

@then('debería ver un mensaje de error indicando que la cantidad debe ser mayor a cero')
def step_then_should_see_quantity_error(context):
    alert = WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    actual_message = alert.text
    if "La cantidad debe ser mayor a cero" not in actual_message:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert "La cantidad debe ser mayor a cero" in actual_message
    alert.accept()

@then('debería ver un mensaje de error indicando que el precio debe ser un valor positivo')
def step_then_should_see_price_error(context):
    alert = WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    actual_message = alert.text
    if "El precio debe ser un valor positivo" not in actual_message:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert "El precio debe ser un valor positivo" in actual_message
    alert.accept()

@then('el total debería ser "{expected_total}"')
def step_then_total_should_be(context, expected_total):
    total_field = context.driver.find_element(By.ID, "total")
    actual_total = total_field.get_attribute("value")
    if actual_total != expected_total:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert actual_total == expected_total, f"Expected {expected_total} but got {actual_total}"

def create_pdf(context, status):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"E:/Documentos Personales/Descargas/02_UC002/reports/results_{timestamp}.pdf"  # Ajusta la ruta de guardado

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Título del reporte
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, "Resultados de las Pruebas - Gestionar Ventas")
    c.setFont("Helvetica", 10)
    result_text = f"Feature: {context.feature.name}\nScenario: {context.scenario.name}\nStatus: {'Passed' if status == 'passed' else 'Failed'}"
    c.drawString(50, height - 100, result_text)
    y_position = height - 130

    # Captura antes de la ejecución
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Antes de la ejecución")
    y_position -= 3

    if os.path.exists(SCREENSHOT_PATH):
        try:
            image = Image.open(SCREENSHOT_PATH)
            image_width, image_height = image.size
            max_width = width - 200
            max_height = height - 250
            if image_width > max_width or image_height > max_height:
                aspect_ratio = image_width / image_height
                if image_width > max_width:
                    image_width = max_width
                    image_height = image_width / aspect_ratio
                if image_height > max_height:
                    image_height = max_height
                    image_width = image_height * aspect_ratio
            c.drawImage(SCREENSHOT_PATH, 50, y_position - image_height, width=image_width, height=image_height)
            y_position -= image_height + 20
        except Exception as e:
            print(f"Error al abrir la imagen para el PDF: {e}")

    # Captura después de la ejecución
    c.setFont("Helvetica", 10)
    c.drawString(50, y_position, "Después de la ejecución")
    y_position -= 3

    if os.path.exists(SCREENSHOT_PATH2):
        try:
            image = Image.open(SCREENSHOT_PATH2)
            image_width, image_height = image.size
            max_width = width - 200
            max_height = height - 250
            if image_width > max_width or image_height > max_height:
                aspect_ratio = image_width / image_height
                if image_width > max_width:
                    image_width = max_width
                    image_height = image_width / aspect_ratio
                if image_height > max_height:
                    image_height = max_height
                    image_width = image_height * aspect_ratio
            c.drawImage(SCREENSHOT_PATH2, 50, y_position - image_height, width=image_width, height=image_height)
        except Exception as e:
            print(f"Error al abrir la imagen para el PDF: {e}")

    c.save()
