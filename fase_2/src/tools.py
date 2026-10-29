import json
from pathlib import Path
from datetime import date, datetime

import pandas as pd


# Ruta base de la fase 2
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

PEDIDOS_FILE = DATA_DIR / "pedidos.json"
PRODUCTOS_FILE = DATA_DIR / "productos.csv"


def cargar_pedidos():
    """Carga los pedidos simulados de EcoMarket."""
    with open(PEDIDOS_FILE, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_productos():
    """Carga el catálogo de productos de EcoMarket."""
    return pd.read_csv(PRODUCTOS_FILE)


def buscar_pedido(pedido_id):
    """Busca un pedido por su identificador."""
    pedidos = cargar_pedidos()

    for pedido in pedidos:
        if pedido["pedido_id"].upper() == pedido_id.upper():
            return pedido

    return None


def buscar_producto(producto_id):
    """Busca un producto por su identificador."""
    productos = cargar_productos()

    producto = productos[
        productos["Código del producto"].astype(str).str.upper()
        == producto_id.upper()
    ]

    if producto.empty:
        return None

    return producto.iloc[0].to_dict()


def verificar_elegibilidad_devolucion(pedido_id, producto_id):
    """
    Verifica si un producto asociado a un pedido es elegible
    para devolución según las reglas de EcoMarket.
    """

    pedido = buscar_pedido(pedido_id)

    if pedido is None:
        return {
            "elegible": False,
            "motivo": f"El pedido {pedido_id} no existe."
        }

    if pedido["producto_id"].upper() != producto_id.upper():
        return {
            "elegible": False,
            "motivo": (
                f"El producto {producto_id} no pertenece "
                f"al pedido {pedido_id}."
            )
        }

    producto = buscar_producto(producto_id)

    if producto is None:
        return {
            "elegible": False,
            "motivo": f"El producto {producto_id} no existe."
        }

    if pedido["estado"].lower() != "entregado":
        return {
            "elegible": False,
            "motivo": (
                "El pedido todavía no ha sido entregado. "
                "La devolución solo puede iniciarse después de la entrega."
            )
        }

    fecha_compra = datetime.strptime(
        pedido["fecha_compra"],
        "%Y-%m-%d"
    ).date()

    dias_transcurridos = (date.today() - fecha_compra).days

    if dias_transcurridos > 30:
        return {
            "elegible": False,
            "motivo": (
                "El pedido se encuentra fuera del plazo "
                "máximo de 30 días para devoluciones."
            )
        }

    admite_devolucion = str(
        producto["Admite devolución"]
    ).strip().lower()

    if admite_devolucion not in ["sí", "si", "true"]:
        return {
            "elegible": False,
            "motivo": (
                f"El producto no admite devolución. "
                f"Condición: {producto['Condición de devolución']}."
            )
        }

    return {
        "elegible": True,
        "motivo": (
            "El producto cumple las condiciones de devolución "
            "de EcoMarket."
        ),
        "pedido_id": pedido["pedido_id"],
        "producto_id": producto_id,
        "producto": producto["Nombre del producto"],
        "categoria": producto["Categoría"]
    }
