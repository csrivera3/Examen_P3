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
SCREENSHOT_PATH = os.path.join(os.getcwd(), "inventario_screenshot_before.png")
SCREENSHOT_PATH2 = os.path.join(os.getcwd(), "inventario_screenshot_after.png")

# Inicia el navegador y abre la aplicación
@given('la aplicación de inventarios está abierta')
def step_given_application_is_open(context):
    context.driver = webdriver.Chrome()
    context.driver.get('E:/Documentos Personales/Escritorio/QUINTO/EXAMEN_3P/Caso 001/Principal/index.html') 
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "tabla-inventario"))
    )  # Espera hasta que la tabla de inventario esté presente
    screenshot = ImageGrab.grab()
    screenshot.save(SCREENSHOT_PATH)

@when('ingreso "{value}" en el campo "{field_id}"')
def step_when_input_value(context, value, field_id):
    field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    field.clear()
    field.send_keys(value)

@when('hago clic en "Agregar Producto"')
def step_when_click_agregar_producto(context):
    button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'agregar-producto'))
    )
    button.click()
    time.sleep(1)  # Espera para asegurar que el producto se agregue
    screenshot = ImageGrab.grab()
    screenshot.save(SCREENSHOT_PATH2)

@then('debería ver el producto "{product_name}" con cantidad "{quantity}" y precio "{price}" en la lista de inventario')
def step_then_should_see_product_in_inventory(context, product_name, quantity, price):
    table = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "tabla-inventario"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")
    found = False
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 0 and cols[0].text == product_name and cols[1].text == quantity and cols[2].text == price:
            found = True
            break
    if not found:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert found, f"El producto {product_name} con cantidad {quantity} y precio {price} no fue encontrado en la lista de inventario."

@then('debería ver un mensaje de error indicando que el nombre del producto es obligatorio')
def step_then_should_see_name_error(context):
    alert = WebDriverWait(context.driver, 10).until(EC.alert_is_present())
    actual_message = alert.text
    if "El nombre del producto es obligatorio" not in actual_message:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert "El nombre del producto es obligatorio" in actual_message
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

@then('el producto "{product_name}" no debería estar en la lista de inventario')
def step_then_product_should_not_be_in_inventory(context, product_name):
    table = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "tabla-inventario"))
    )
    rows = table.find_elements(By.TAG_NAME, "tr")
    found = False
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) > 0 and cols[0].text == product_name:
            found = True
            break
    if found:
        create_pdf(context, "failed")
    else:
        create_pdf(context, 'passed')
    assert not found, f"El producto {product_name} aún está presente en la lista de inventario."

def create_pdf(context, status):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"E:/Documentos Personales/Escritorio/QUINTO/EXAMEN_3P/Caso 001/reports/results_{timestamp}.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Título del reporte
    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, "Resultados de las Pruebas - Gestionar Inventarios")
    c.setFont("Helvetica", 10)
    result_text = f"Feature: Pasos.feature\nStatus: {'Passed' if status == 'passed' else 'Failed'}"
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
