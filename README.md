# EcoMarket AI Agent

Proyecto Final - Agente de IA para automatización de devoluciones en EcoMarket.

## Descripción

Este proyecto extiende la arquitectura RAG desarrollada previamente para EcoMarket
e incorpora un agente de inteligencia artificial capaz de interpretar solicitudes,
consultar información y ejecutar acciones relacionadas con el proceso de devolución
de productos.

El agente puede:

- responder consultas informativas mediante RAG;
- verificar si un producto es elegible para devolución;
- generar una etiqueta de devolución;
- manejar pedidos inexistentes;
- explicar motivos de rechazo;
- seleccionar automáticamente la herramienta adecuada según la intención del usuario.

## Arquitectura general

El flujo principal del sistema es:

Usuario  
↓  
Interfaz Streamlit  
↓  
Agente EcoMarket  
↓  
Selección de herramienta  
↓  
Ejecución de la herramienta  
↓  
Respuesta final al usuario

El agente utiliza tres herramientas principales:

- `consultar_ecomarket`
- `verificar_devolucion`
- `generar_etiqueta`

## Tecnologías utilizadas

- Python
- LangChain
- Gemini
- Streamlit
- ChromaDB
- Sentence Transformers
- Hugging Face Embeddings
- Pandas

## Estructura del repositorio

### Fase 1 - Diseño de arquitectura

Contiene la conceptualización del agente, la selección del framework, la definición
de herramientas y el diagrama de arquitectura.

Archivo principal:

`fase_1/arquitectura_agente.md`

### Fase 2 - Implementación

Contiene la lógica del agente, las herramientas, los datos simulados y la integración
con RAG.

Archivos principales:

- `fase_2/src/agent.py`
- `fase_2/src/tools.py`
- `fase_2/src/rag_tool.py`
- `fase_2/src/test_tools.py`

Datos utilizados:

- `pedidos.json`
- `productos.csv`
- `politica_devoluciones.md`
- `faq.json`
- `envios.md`

### Fase 3 - Análisis crítico

Incluye el análisis de:

- riesgos éticos;
- seguridad;
- prompt injection;
- privacidad;
- monitoreo;
- observabilidad;
- intervención humana;
- propuestas de mejora.

Archivo principal:

`fase_3/analisis_critico.md`

### Fase 4 - Despliegue

Contiene la aplicación web desarrollada en Streamlit.

Archivo principal:

`fase_4/app.py`

## Flujo del proceso de devolución

1. El usuario realiza una solicitud.
2. El agente interpreta la intención.
3. Si es una consulta informativa, utiliza RAG.
4. Si es una devolución, verifica elegibilidad.
5. Si la devolución es aprobada, genera la etiqueta.
6. Si la devolución es rechazada, informa el motivo.
7. La respuesta final se muestra al usuario mediante Streamlit.

## Reglas de negocio

La validación de devoluciones considera:

- existencia del pedido;
- correspondencia entre pedido y producto;
- estado de entrega;
- plazo máximo de 30 días;
- elegibilidad del producto;
- restricciones por categoría.

Las decisiones críticas se realizan mediante funciones determinísticas y no dependen
únicamente del modelo generativo.

## Casos de prueba

### Devolución aprobada

`Quiero devolver el producto P001 del pedido ECO1001.`

Resultado: La devolución es aprobada y se genera una etiqueta.

### Devolución rechazada

`Quiero devolver el producto P002 del pedido ECO1002.`

Resultado: La devolución es rechazada porque el producto es de higiene personal.

### Pedido inexistente

`Quiero devolver el producto P001 del pedido ECO9999.`

Resultado: El sistema informa que el pedido no existe.

### Consulta informativa

`¿Puedo devolver un alimento?`

Resultado: El agente utiliza RAG y responde con base en la política de devoluciones de EcoMarket.

## Ejecución

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar la variable de entorno:

```text
GEMINI_API_KEY
```

Ejecutar la aplicación:

```bash
streamlit run fase_4/app.py
```

## Resultado

La solución integra RAG, herramientas, reglas de negocio, un agente con tool calling
y una interfaz web funcional.

El proyecto demuestra cómo un asistente basado únicamente en recuperación de
información puede evolucionar hacia un sistema agentivo capaz de interpretar
solicitudes, seleccionar herramientas y ejecutar acciones de manera controlada.

## Mejoras futuras

Como evolución del proyecto se propone:

- integración con CRM;
- conexión con servicios reales de logística;
- persistencia en base de datos;
- monitoreo y observabilidad;
- auditoría de acciones;
- confirmación humana para operaciones críticas.
