import sys
from pathlib import Path

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


# Configuración de rutas


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "fase_2" / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))


# Importar agente

from agent import crear_agente


# Configuración de la página

st.set_page_config(
    page_title="EcoMarket AI Agent",
    page_icon="🤖",
    layout="centered"
)

st.title("EcoMarket AI Agent")

st.write(
    """
    Asistente inteligente para consultas y gestión de devoluciones.
    El agente puede consultar información de EcoMarket, verificar la
    elegibilidad de una devolución y generar una etiqueta cuando corresponda.
    """
)

# Inicializar modelo y agente

@st.cache_resource
def inicializar_agente():
    modelo = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0
    )

    return crear_agente(modelo)


try:
    agente = inicializar_agente()

except Exception as error:
    st.error(
        "No fue posible inicializar el agente. "
        "Verifica la configuración de la API key."
    )

    st.exception(error)
    st.stop()

# Función para extraer el texto final

def extraer_texto_respuesta(resultado):
    mensaje_final = resultado["messages"][-1]
    contenido = mensaje_final.content

    if isinstance(contenido, list):
        textos = []

        for bloque in contenido:
            if isinstance(bloque, dict) and "text" in bloque:
                textos.append(bloque["text"])

        return "\n".join(textos)

    return str(contenido)

# Interfaz

st.subheader("Consulta")

consulta = st.text_area(
    "Escribe tu consulta:",
    placeholder=(
        "Ejemplo: Quiero devolver el producto P001 "
        "del pedido ECO1001."
    ),
    height=120
)


if st.button("Enviar consulta"):

    if not consulta.strip():
        st.warning("Por favor, escribe una consulta.")

    else:
        with st.spinner("Procesando solicitud..."):

            try:

                resultado = agente.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": consulta
                            }
                        ]
                    }
                )

                respuesta = extraer_texto_respuesta(resultado)

                st.subheader("Respuesta del agente")

                st.success(respuesta)

            except Exception as error:

                st.error(
                    "Ocurrió un error al procesar la solicitud."
                )

                st.exception(error)


# Ejemplos

st.divider()

st.subheader("Ejemplos de prueba")

st.markdown(
    """
    **Consulta informativa**

    `¿Puedo devolver un alimento?`

    **Devolución aprobada**

    `Quiero devolver el producto P001 del pedido ECO1001.`

    **Devolución rechazada**

    `Quiero devolver el producto P002 del pedido ECO1002.`

    **Pedido inexistente**

    `Quiero devolver el producto P001 del pedido ECO9999.`
    """
)
