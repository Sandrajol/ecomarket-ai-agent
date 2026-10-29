from tools import verificar_elegibilidad_devolucion


casos_prueba = [
    ("ECO1001", "P001"),
    ("ECO1002", "P002"),
    ("ECO1003", "P007"),
    ("ECO1004", "P009"),
    ("ECO9999", "P001"),
]


for pedido_id, producto_id in casos_prueba:
    print("=" * 60)
    print(f"Pedido: {pedido_id} | Producto: {producto_id}")

    resultado = verificar_elegibilidad_devolucion(
        pedido_id,
        producto_id
    )

    print(resultado)
