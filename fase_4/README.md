# Fase 4
# Despliegue de la Aplicación

## 1. Objetivo

En esta fase se desplegó el agente de EcoMarket mediante una interfaz web simple
utilizando Streamlit.

La aplicación permite que un usuario final interactúe con el agente mediante
consultas en lenguaje natural.

El agente puede:

- responder preguntas informativas mediante RAG;
- verificar si una devolución es elegible;
- generar una etiqueta de devolución;
- manejar pedidos inexistentes;
- explicar motivos de rechazo.

## 2. Selección de Streamlit

Para construir la interfaz se seleccionó Streamlit.

La elección se realizó por las siguientes razones:

- integración sencilla con aplicaciones desarrolladas en Python;
- facilidad para construir interfaces sin necesidad de desarrollar frontend
  adicional;
- permite visualizar respuestas de manera clara;
- facilita la ejecución del agente desde una interfaz web;
- permite realizar pruebas y demostraciones de forma rápida.

Gradio también era una alternativa válida, pero Streamlit ofrece una estructura
más flexible para presentar los diferentes componentes de la aplicación.

## 3. Interfaz

La interfaz contiene:

- título de la aplicación;
- descripción del agente;
- campo de texto para ingresar la consulta;
- botón para enviar la solicitud;
- área de visualización de la respuesta;
- ejemplos de consultas de prueba.

El archivo principal de la aplicación es: `app.py`

## 4. Integración con el agente

La aplicación importa el agente desarrollado en la Fase 2.

El flujo de ejecución es:

Usuario  
↓  
Streamlit  
↓  
Agente EcoMarket  
↓  
Selección de herramienta  
↓  
Ejecución de la herramienta  
↓  
Respuesta final  
↓  
Visualización en la interfaz

## 5. Casos de prueba

### Devolución aprobada

Consulta: `Quiero devolver el producto P001 del pedido ECO1001.`

Resultado: La devolución es aprobada y el agente genera una etiqueta de devolución.

Código generado: `ECO-RETURN-ECO1001-P001`

### Devolución rechazada

Consulta: `Quiero devolver el producto P002 del pedido ECO1002.`

Resultado: El agente informa que el producto no admite devolución por corresponder a un
producto de higiene personal.

No se genera etiqueta.

### Pedido inexistente

Consulta: `Quiero devolver el producto P001 del pedido ECO9999.`

Resultado: El agente informa que el pedido no existe y no continúa con el proceso de
devolución.

### Consulta informativa

Consulta: `¿Puedo devolver un alimento?`

Resultado: El agente utiliza la herramienta RAG para consultar la base de conocimiento de
EcoMarket e informa que los productos perecederos no son elegibles para
devolución.

## 6. Manejo de errores

La aplicación incorpora manejo básico de errores.

Si ocurre un problema durante la inicialización del agente o durante una consulta,
la interfaz muestra un mensaje de error al usuario.

Además, las reglas críticas de devolución permanecen dentro de las herramientas
determinísticas y no dependen únicamente del modelo de lenguaje.

## 7. Resultado

Las pruebas realizadas demostraron que la aplicación funciona de extremo a
extremo.

El usuario puede ingresar una consulta desde la interfaz, el agente interpreta la
solicitud, selecciona la herramienta adecuada, ejecuta la acción y presenta una
respuesta clara en Streamlit.

## 8. Conclusión

El despliegue mediante Streamlit permite convertir la arquitectura desarrollada
en las fases anteriores en una aplicación accesible para un usuario final.

La solución integra RAG, herramientas, reglas de negocio y un agente de lenguaje
dentro de una interfaz web funcional.
