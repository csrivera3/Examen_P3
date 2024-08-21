Feature: Gestionar Ventas

  Scenario: Realizar una venta exitosa
    Given la aplicación de ventas está abierta
    When selecciono "Producto 1" en el campo "producto"
    And ingreso "3" en el campo "cantidad"
    And ingreso "20.00" en el campo "precio"
    And hago clic en "Gestionar Venta"
    Then debería ver un mensaje de éxito indicando que la venta se gestionó correctamente
    And el total debería ser "60.00"

  Scenario: Intentar realizar una venta sin seleccionar un producto
    Given la aplicación de ventas está abierta
    When selecciono "" en el campo "producto"
    And ingreso "3" en el campo "cantidad"
    And ingreso "20.00" en el campo "precio"
    And hago clic en "Gestionar Venta"
    Then debería ver un mensaje de error indicando que se debe seleccionar un producto

  Scenario: Intentar realizar una venta con cantidad cero
    Given la aplicación de ventas está abierta
    When selecciono "Producto 1" en el campo "producto"
    And ingreso "0" en el campo "cantidad"
    And ingreso "20.00" en el campo "precio"
    And hago clic en "Gestionar Venta"
    Then debería ver un mensaje de error indicando que la cantidad debe ser mayor a cero

  Scenario: Intentar realizar una venta con precio negativo
    Given la aplicación de ventas está abierta
    When selecciono "Producto 1" en el campo "producto"
    And ingreso "3" en el campo "cantidad"
    And ingreso "-5.00" en el campo "precio"
    And hago clic en "Gestionar Venta"
    Then debería ver un mensaje de error indicando que el precio debe ser un valor positivo
