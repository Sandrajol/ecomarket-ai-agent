# FASE 1
# DISEÑO DE LA ARQUITECTURA DEL AGENTE

## 1. Introducción

En los talleres anteriores se desarrolló para EcoMarket una solución basada en
Retrieval Augmented Generation (RAG), capaz de consultar información interna de
la empresa antes de generar respuestas para los usuarios.
El proyecto final extiende esta arquitectura incorporando un agente de inteligencia 
artificial capaz de ejecutar acciones de manera autónoma.

El agente podrá:

- Consultar información de EcoMarket;
- Verificar si un producto es elegible para devolución;
- Generar una etiqueta de devolución cuando se cumplan las condiciones;
- Responder de manera clara al usuario;
- Manejar situaciones en las que la devolución no sea posible.

## 2. Arquitectura propuesta

Se propone una arquitectura agentiva en la que el modelo de lenguaje actúa como
orquestador del proceso. El agente recibe la consulta del usuario, analiza la 
intención y decide qué herramienta utilizar.

La arquitectura tendrá tres capacidades principales:
1. Consultar la base de conocimiento mediante RAG.
2. Verificar la elegibilidad de una devolución.
3. Generar una etiqueta de devolución.

El flujo general será:

Usuario -> Agente EcoMarket -> Análisis de la intención -> Selección de herramienta ↓
                     Respuesta al usuario <- Resultado <- Ejecución de la herramienta 
  
  
## 3. Integración del sistema RAG

El sistema RAG desarrollado en el Taller 2 se conservará como una herramienta
del agente. Esta herramienta permitirá responder preguntas relacionadas con:políticas de devolución,
información de productos, preguntas frecuentes, información sobre envíos.

# FLUJO

Pregunta del usuario -> Modelo de embeddings -> ChromaDB -> Retriever -> Fragmentos relevantes -> Respuesta del agente

La principal ventaja de mantener RAG como una herramienta es que el agente puede
decidir cuándo necesita consultar información documental y cuándo debe ejecutar
una acción específica.

## 4. Herramientas del agente

### 4.1 Herramienta 1: consultar_conocimiento_ecomarket

Objetivo: Consultar la base de conocimiento de EcoMarket mediante la arquitectura RAG.

Entrada: pregunta del usuario.

Proceso: generar el embedding de la consulta, recuperar los fragmentos relevantes desde ChromaDB y
utilizar los fragmentos como contexto para responder.

Salida: información relevante recuperada desde la base de conocimiento.

### Ejemplo: 

Pregunta: "¿Cuál es la política de devolución de alimentos?"

Salida: "Los productos perecederos, como alimentos y flores, no son elegibles para
devolución."

### 4.2 Herramienta 2: verificar_elegibilidad_devolucion

Objetivo: Determinar si un producto asociado a un pedido puede ser devuelto.

Entradas: identificador del pedido e identificador del producto.

La herramienta consultará los datos del pedido y del producto para verificar:

- que el pedido exista;
- que el producto pertenezca al pedido;
- que el pedido haya sido entregado;
- que la solicitud se encuentre dentro del plazo permitido;
- que el producto sea retornable;
- que no pertenezca a una categoría excluida.

Salida: La herramienta devolverá una respuesta estructurada con:
- estado de elegibilidad;
- motivo de aprobación o rechazo;
- información básica del pedido y del producto.

### Ejemplo de salida:

Elegible: Sí

Motivo: "El producto se encuentra dentro del plazo permitido y cumple las condiciones
de devolución de EcoMarket."

### 4.3 Herramienta 3: generar_etiqueta_devolucion

Objetivo: Generar una etiqueta de devolución para los productos previamente aprobados.

Entradas: identificador del pedido e identificador del producto.

Condición: La herramienta solamente podrá generar una etiqueta cuando la devolución haya
sido aprobada previamente.

Salida: Una etiqueta con información como:

- Código de devolución;
- Identificador del pedido;
- Producto;
- Transportadora;
- Destino de devolución;
- Estado de autorización.

### Ejemplo:

Código de devolución: ECO-RETURN-001

Pedido: ECO1001

Producto: Botella reutilizable de acero inoxidable

Transportadora: Servientrega

Estado: AUTORIZADA

## 5. Selección del framework

Para implementar el agente se selecciona LangChain.

La elección se fundamenta en los siguientes aspectos:

- Ya la utilizamos en el Taller 2 para integrar los componentes del sistema RAG
- Permite definir herramientas que pueden ser utilizadas por agentes
- Facilita la conexión entre modelos de lenguaje, prompts, herramientas y bases
  vectoriales
- Permite construir flujos agentivos de manera modular
- Reduce la necesidad de introducir un framework completamente nuevo para el
  proyecto final.

LlamaIndex también permite implementar agentes y herramientas, pero para este
proyecto LangChain ofrece continuidad con el trabajo desarrollado previamente y
reduce la complejidad de integración.

## 6. Flujo de decisiones del agente

El agente analizará la consulta del usuario y determinará la acción adecuada.

### Caso 1: consulta informativa

Ejemplo:"¿Cuántos días tengo para devolver un producto?"

El agente utilizará:`consultar_conocimiento_ecomarket`

y responderá utilizando la información recuperada desde la base RAG.

### Caso 2: solicitud de devolución

Ejemplo: "Quiero devolver el producto P001 del pedido ECO1001."

El agente utilizará: `verificar_elegibilidad_devolucion`

Si se aprueba la  devolución: `generar_etiqueta_devolucion`

Si la devolución es rechazada: El agente explicará al usuario el motivo.

### Caso 3: pedido inexistente

Ejemplo: "Quiero devolver el producto P001 del pedido ECO9999."

La herramienta de elegibilidad detectará que el pedido no existe.

El agente deberá informar el error de forma clara y no generar una etiqueta.

## 7. Flujo general del proceso de devolución

              Usuario solicita devolución  
                         ↓  
              Agente identifica intención  
                         ↓  
              Solicita pedido y producto  
                         ↓  
                Verifica elegibilidad  
                         ↓  
                   ¿Es elegible?
         Sí                           No 
          ↓                           ↓
    Generar etiqueta          Explicar motivo de rechazo  
          ↓                           ↓ 
Responder al usuario con       Finalizar proceso
  aprobación y etiqueta
 
## 8. Consideraciones de seguridad

Las decisiones críticas del proceso de devolución no dependerán exclusivamente
del modelo de lenguaje.

El LLM será responsable de interpretar la intención del usuario y seleccionar
la herramienta adecuada.

Sin embargo, la decisión de elegibilidad será realizada mediante reglas
determinísticas implementadas en la herramienta
`verificar_elegibilidad_devolucion`.

De esta manera se reduce el riesgo de que el modelo apruebe una devolución debido
a una alucinación o a una instrucción maliciosa del usuario.
Asi mismo, la herramienta `generar_etiqueta_devolucion` solamente podrá ejecutarse
cuando exista una autorización válida.

## 9. Conclusión

La arquitectura propuesta permite evolucionar el sistema desarrollado en los
talleres anteriores desde un asistente basado en RAG hacia un agente capaz de
consultar información y ejecutar acciones.

La separación entre el modelo de lenguaje y las reglas de negocio permite mantener
la flexibilidad de la inteligencia artificial para interpretar solicitudes, al
mismo tiempo que las decisiones críticas se ejecutan mediante reglas controladas.

Esta combinación permite construir una solución más segura, modular y adecuada
para automatizar el proceso de devoluciones de EcoMarket.
