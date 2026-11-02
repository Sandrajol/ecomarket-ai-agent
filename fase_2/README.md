# Fase 2
# Implementación y Conexión de Componentes

## 1. Objetivo

En esta fase se implementó el agente de EcoMarket a partir de la arquitectura
definida en la Fase 1.

El sistema integra el RAG desarrollado previamente con nuevas herramientas
orientadas a automatizar el proceso de devolución de productos.

El agente utiliza un modelo de lenguaje para interpretar la intención del usuario
y decidir qué herramienta debe ejecutar.

## 2. Estructura de datos

Se utilizaron los siguientes archivos:

- `pedidos.json`: contiene pedidos simulados de EcoMarket.
- `productos.csv`: contiene el catálogo de productos.
- `politica_devoluciones.md`: contiene las políticas de devolución.
- `faq.json`: contiene preguntas frecuentes.
- `envios.md`: contiene información relacionada con envíos.

Los datos simulados permiten evaluar diferentes escenarios, como:

- devolución aprobada;
- producto no retornable;
- producto perecedero;
- pedido fuera del plazo permitido;
- pedido no entregado;
- pedido inexistente.

## 3. Herramienta de verificación de elegibilidad

La función:

`verificar_elegibilidad_devolucion()`

determina si un producto puede ser devuelto.

La herramienta verifica:

- existencia del pedido;
- relación entre pedido y producto;
- existencia del producto;
- estado de entrega;
- plazo máximo de 30 días;
- condición de devolución del producto.

La decisión se realiza mediante reglas determinísticas y no depende únicamente
del modelo de lenguaje.

Esto permite reducir el riesgo de aprobar devoluciones incorrectas debido a una
alucinación del modelo.

## 4. Herramienta de generación de etiqueta

La función:

`generar_etiqueta_devolucion()`

genera una etiqueta solamente cuando la devolución fue previamente aprobada.

La etiqueta contiene:

- código de devolución;
- identificador del pedido;
- identificador del producto;
- nombre del producto;
- categoría;
- transportadora;
- destino;
- estado de autorización.

Si la devolución no es elegible, la herramienta no genera ninguna etiqueta.

## 5. Herramienta RAG

Se reutilizó la arquitectura RAG del Taller 2 mediante la función:

`consultar_conocimiento_ecomarket()`

La herramienta utiliza:

- carga de documentos;
- chunking;
- embeddings;
- ChromaDB;
- retriever.

El modelo de embeddings utilizado es:

`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

El retriever recupera los tres fragmentos más relevantes para cada consulta.

Esta herramienta es utilizada por el agente cuando el usuario realiza preguntas
informativas sobre políticas, productos, envíos o preguntas frecuentes.

## 6. Integración del agente

El agente se implementó con LangChain.

Se definieron tres tools:

- `consultar_ecomarket`
- `verificar_devolucion`
- `generar_etiqueta`

El agente utiliza un modelo de lenguaje compatible con tool calling para decidir
qué herramienta debe ejecutar según la intención del usuario.

El flujo principal es:

Consulta del usuario  
↓  
Interpretación de la intención  
↓  
Selección de herramienta  
↓  
Ejecución  
↓  
Resultado de la herramienta  
↓  
Respuesta final al usuario

## 7. Modelo de lenguaje

Para el agente se utiliza Gemini mediante la integración con LangChain.

El modelo se encarga de:

- interpretar la intención del usuario;
- seleccionar la herramienta adecuada;
- solicitar información faltante;
- encadenar herramientas cuando sea necesario;
- generar una respuesta clara y amigable.

Las reglas críticas del proceso de devolución permanecen en las funciones
determinísticas y no en el modelo de lenguaje.

## 8. Pruebas realizadas

Se probaron diferentes escenarios.

### Caso exitoso

Pedido: `ECO1001`

Producto: `P001`

Resultado: La devolución fue aprobada y el agente generó una etiqueta de devolución.

### Producto no retornable

Pedido: `ECO1002`

Producto: `P002`

Resultado: La devolución fue rechazada porque corresponde a un producto de higiene personal.

No se generó etiqueta.

### Producto perecedero

Pedido: `ECO1003`

Producto: `P007`

Resultado: La devolución fue rechazada porque el producto es perecedero.

### Pedido fuera del plazo permitido

Pedido: `ECO1004`

Producto: `P009`

Resultado: La devolución fue rechazada porque se encontraba fuera del plazo máximo de 30 días.

### Pedido inexistente

Pedido: `ECO9999`

Producto: `P001`

Resultado: El agente informó que el pedido no existe y no generó una etiqueta.

### Consulta informativa

Pregunta: `¿Puedo devolver un alimento?`

Resultado: El agente utilizó la herramienta RAG y respondió utilizando la información
recuperada desde la base de conocimiento de EcoMarket.

## 9. Comportamiento del agente

Las pruebas demostraron que el agente es capaz de distinguir entre:

- consultas informativas;
- solicitudes de devolución;
- casos elegibles;
- casos no elegibles;
- errores en los datos.

También se verificó que una devolución rechazada no puede continuar hacia la
generación de una etiqueta.

## 10. Conclusión

La implementación integra exitosamente la arquitectura RAG desarrollada en el
Taller 2 con un agente capaz de ejecutar acciones.

La separación entre el razonamiento del modelo y las reglas determinísticas
permite mantener flexibilidad en la interacción con el usuario sin comprometer
las decisiones críticas del proceso de devolución.

El agente es capaz de seleccionar herramientas, ejecutar acciones y manejar tanto
casos exitosos como fallidos.
