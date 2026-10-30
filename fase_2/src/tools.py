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
        productos["codigo_producto"].astype(str).str.upper()
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
        producto["admite_devolucion"]
    ).strip().lower()

    if admite_devolucion not in ["sí", "si", "true"]:
        return {
            "elegible": False,
            "motivo": (
                f"El producto no admite devolución. "
                f"Condición: {producto['condicion_devolucion']}."
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
        "producto": producto["nombre_producto"],
        "categoria": producto["categoria"]
    }

def generar_etiqueta_devolucion(pedido_id, producto_id):
    """
    Genera una etiqueta de devolución únicamente si el producto
    es elegible para devolución.
    """

    resultado_elegibilidad = verificar_elegibilidad_devolucion(
        pedido_id,
        producto_id
    )

    if not resultado_elegibilidad["elegible"]:
        return {
            "generada": False,
            "motivo": (
                "No se puede generar la etiqueta porque la devolución "
                "no fue aprobada. "
                + resultado_elegibilidad["motivo"]
            )
        }

    codigo_devolucion = f"ECO-RETURN-{pedido_id}-{producto_id}"

    etiqueta = {
        "codigo_devolucion": codigo_devolucion,
        "pedido_id": pedido_id,
        "producto_id": producto_id,
        "producto": resultado_elegibilidad["producto"],
        "categoria": resultado_elegibilidad["categoria"],
        "transportadora": "Servientrega",
        "destino": "Centro de Devoluciones EcoMarket",
        "estado": "AUTORIZADA"
    }

    return {
        "generada": True,
        "mensaje": "Etiqueta de devolución generada correctamente.",
        "etiqueta": etiqueta
    }




