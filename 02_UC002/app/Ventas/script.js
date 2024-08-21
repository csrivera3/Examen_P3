function gestionarVenta() {
    const producto = document.getElementById('producto').value;
    const cantidad = document.getElementById('cantidad').value;
    const precio = document.getElementById('precio').value;

    if (!producto) {
        alert("Debe seleccionar un producto.");
        return;
    }

    if (cantidad <= 0) {
        alert("La cantidad debe ser mayor a cero.");
        return;
    }

    if (precio <= 0) {
        alert("El precio debe ser un valor positivo.");
        return;
    }

    const total = cantidad * precio;
    document.getElementById('total').value = total.toFixed(2);

    alert(`Venta gestionada exitosamente. Total: $${total.toFixed(2)}`);
    // Aquí se puede agregar la lógica para actualizar la base de datos o realizar otras acciones.
}
