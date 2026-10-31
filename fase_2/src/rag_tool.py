from pathlib import Path
import json
import pandas as pd

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def cargar_base_conocimiento():
    """
    Carga los documentos de EcoMarket que serán utilizados
    por la herramienta RAG.
    """

    documentos = []

    # Política de devoluciones
    politica_path = DATA_DIR / "politica_devoluciones.md"

    with open(politica_path, "r", encoding="utf-8") as archivo:
        documentos.append(
            Document(
                page_content=archivo.read(),
                metadata={
                    "fuente": "politica_devoluciones.md",
                    "tipo": "politica_devoluciones"
                }
            )
        )

    # Información de envíos
    envios_path = DATA_DIR / "envios.md"

    with open(envios_path, "r", encoding="utf-8") as archivo:
        documentos.append(
            Document(
                page_content=archivo.read(),
                metadata={
                    "fuente": "envios.md",
                    "tipo": "envios"
                }
            )
        )

    # Preguntas frecuentes
    faq_path = DATA_DIR / "faq.json"

    with open(faq_path, "r", encoding="utf-8") as archivo:
        preguntas = json.load(archivo)

    for item in preguntas:
        contenido = (
            f"Pregunta: {item['pregunta']}\n"
            f"Respuesta: {item['respuesta']}"
        )

        documentos.append(
            Document(
                page_content=contenido,
                metadata={
                    "fuente": "faq.json",
                    "tipo": "pregunta_frecuente"
                }
            )
        )

    # Productos
    productos_path = DATA_DIR / "productos.csv"
    productos = pd.read_csv(productos_path)

    for _, producto in productos.iterrows():
        contenido = (
            f"Código del producto: {producto['codigo_producto']}\n"
            f"Nombre del producto: {producto['nombre_producto']}\n"
            f"Categoría: {producto['categoria']}\n"
            f"Disponibilidad: {producto['disponibilidad']}\n"
            f"Admite devolución: {producto['admite_devolucion']}\n"
            f"Condición de devolución: {producto['condicion_devolucion']}"
        )

        documentos.append(
            Document(
                page_content=contenido,
                metadata={
                    "fuente": "productos.csv",
                    "tipo": "producto"
                }
            )
        )

    return documentos
