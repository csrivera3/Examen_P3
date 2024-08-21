document.getElementById('inventory-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const productName = document.getElementById('product-name').value;
    const productQuantity = document.getElementById('product-quantity').value;
    const productPrice = document.getElementById('product-price').value;

    if (!productName) {
        alert('El nombre del producto es obligatorio');
        return;
    }

    if (productQuantity <= 0) {
        alert('La cantidad debe ser mayor a cero');
        return;
    }

    if (productPrice < 0) {
        alert('El precio debe ser un valor positivo');
        return;
    }

    const table = document.getElementById('inventory-list');
    const newRow = table.insertRow();

    const nameCell = newRow.insertCell(0);
    const quantityCell = newRow.insertCell(1);
    const priceCell = newRow.insertCell(2);
    const actionCell = newRow.insertCell(3);

    nameCell.textContent = productName;
    quantityCell.textContent = productQuantity;
    priceCell.textContent = parseFloat(productPrice).toFixed(2);

    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Eliminar';
    deleteButton.addEventListener('click', function() {
        table.deleteRow(newRow.rowIndex - 1);
    });
    actionCell.appendChild(deleteButton);

    // Limpia los campos después de agregar el producto
    document.getElementById('product-name').value = '';
    document.getElementById('product-quantity').value = '';
    document.getElementById('product-price').value = '';
});