Feature: Gestionar Inventarios

  Scenario: Agregar un producto exitosamente
    Given la aplicación de inventarios está abierta
    When ingreso "Producto A" en el campo "Nombre del Producto"
    And ingreso "10" en el campo "Cantidad"
    And ingreso "15.00" en el campo "Precio"
    And hago clic en "Agregar Producto"
    Then debería ver el producto "Producto A" con cantidad "10" y precio "15.00" en la lista de inventario

  Scenario: Intentar agregar un producto sin nombre
    Given la aplicación de inventarios está abierta
    When ingreso "" en el campo "Nombre del Producto"
    And ingreso "10" en el campo "Cantidad"
    And ingreso "15.00" en el campo "Precio"
    And hago clic en "Agregar Producto"
    Then debería ver un mensaje de error indicando que el nombre del producto es obligatorio

  Scenario: Intentar agregar un producto con cantidad cero
    Given la aplicación de inventarios está abierta
    When ingreso "Producto B" en el campo "Nombre del Producto"
    And ingreso "0" en el campo "Cantidad"
    And ingreso "20.00" en el campo "Precio"
    And hago clic en "Agregar Producto"
    Then debería ver un mensaje de error indicando que la cantidad debe ser mayor a cero

  Scenario: Intentar agregar un producto con precio negativo
    Given la aplicación de inventarios está abierta
    When ingreso "Producto C" en el campo "Nombre del Producto"
    And ingreso "5" en el campo "Cantidad"
    And ingreso "-10.00" en el campo "Precio"
    And hago clic en "Agregar Producto"
    Then debería ver un mensaje de error indicando que el precio debe ser un valor positivo

  Scenario: Eliminar un producto del inventario
    Given el producto "Producto A" está en la lista de inventario
    When hago clic en "Eliminar" junto al producto "Producto A"
    Then el producto "Producto A" no debería estar en la lista de inventario