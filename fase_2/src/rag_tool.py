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

def crear_chunks(documentos):
    """
    Divide los documentos en fragmentos pequeños para
    facilitar la recuperación semántica.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80
    )

    chunks = text_splitter.split_documents(documentos)

    return chunks

def crear_vectorstore(chunks):
    """
    Genera embeddings y crea la base vectorial ChromaDB.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="ecomarket"
    )

    return vectorstore

def crear_retriever(vectorstore):
    """
    Configura el retriever para recuperar los tres
    fragmentos más relevantes.
    """

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever

# Retriever reutilizable para evitar reconstruir ChromaDB
# cada vez que el agente realiza una consulta.
_retriever_global = None


def obtener_retriever():
    """
    Inicializa el sistema RAG una sola vez y reutiliza
    el retriever en las siguientes consultas.
    """

    global _retriever_global

    if _retriever_global is None:
        documentos = cargar_base_conocimiento()
        chunks = crear_chunks(documentos)
        vectorstore = crear_vectorstore(chunks)
        _retriever_global = crear_retriever(vectorstore)

    return _retriever_global


def consultar_conocimiento_ecomarket(pregunta):
    """
    Recupera información relevante de la base de conocimiento
    de EcoMarket para una consulta del usuario.
    """

    retriever = obtener_retriever()

    documentos_recuperados = retriever.invoke(pregunta)

    if not documentos_recuperados:
        return (
            "No se encontró información relevante en la base "
            "de conocimiento de EcoMarket."
        )

    contexto = []

    for documento in documentos_recuperados:
        fuente = documento.metadata.get("fuente", "Fuente desconocida")

        contexto.append(
            f"Fuente: {fuente}\n"
            f"{documento.page_content}"
        )

    return "\n\n".join(contexto)








