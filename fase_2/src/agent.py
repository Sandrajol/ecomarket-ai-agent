from langchain.agents import create_agent
from langchain_core.tools import tool

from tools import (
    verificar_elegibilidad_devolucion,
    generar_etiqueta_devolucion
)

from rag_tool import consultar_conocimiento_ecomarket


@tool
def consultar_ecomarket(pregunta: str) -> str:
    """
    Consulta la base de conocimiento de EcoMarket.

    Utiliza esta herramienta para preguntas informativas sobre:
    políticas de devolución, productos, envíos y preguntas frecuentes.
    """
    return consultar_conocimiento_ecomarket(pregunta)


@tool
def verificar_devolucion(pedido_id: str, producto_id: str) -> dict:
    """
    Verifica si un producto asociado a un pedido es elegible
    para devolución.

    Utiliza esta herramienta cuando el usuario solicita devolver
    un producto y proporciona el ID del pedido y del producto.
    """
    return verificar_elegibilidad_devolucion(
        pedido_id,
        producto_id
    )


@tool
def generar_etiqueta(pedido_id: str, producto_id: str) -> dict:
    """
    Genera una etiqueta de devolución únicamente cuando el
    producto cumple las condiciones de devolución.

    Utiliza esta herramienta después de verificar que la
    devolución es elegible.
    """
    return generar_etiqueta_devolucion(
        pedido_id,
        producto_id
    )


tools = [
    consultar_ecomarket,
    verificar_devolucion,
    generar_etiqueta
]


SYSTEM_PROMPT = """
Eres el agente virtual de atención al cliente de EcoMarket.

Tu función es responder consultas y gestionar solicitudes de devolución
utilizando las herramientas disponibles.

Reglas:

1. Para preguntas informativas sobre políticas, productos, envíos o preguntas
   frecuentes, utiliza consultar_ecomarket.

2. Cuando el usuario solicite devolver un producto, necesitas:
   - ID del pedido.
   - ID del producto.

3. Si falta alguno de esos datos, solicita únicamente la información faltante.

4. Cuando tengas pedido y producto, utiliza verificar_devolucion.

5. Si la devolución NO es elegible:
   - no utilices generar_etiqueta;
   - explica claramente el motivo al usuario.

6. Si la devolución ES elegible:
   - utiliza generar_etiqueta;
   - informa al usuario que la devolución fue autorizada;
   - incluye el código de devolución generado.

7. Nunca inventes pedidos, productos, políticas ni autorizaciones.

8. No apruebes una devolución por tu cuenta. La decisión válida es únicamente
   la que devuelve verificar_devolucion.

9. Responde siempre en español, de manera clara, breve y amable.
"""


def crear_agente(modelo):
    """
    Crea el agente EcoMarket utilizando LangChain.
    """

    agente = create_agent(
        model=modelo,
        tools=tools,
        system_prompt=SYSTEM_PROMPT
    )

    return agente
