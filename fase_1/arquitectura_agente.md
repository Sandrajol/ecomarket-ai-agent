# FASE 1: DISEÑO DE LA ARQUITECTURA DEL AGENTE

## Proyecto Final - EcoMarket

El objetivo de esta fase es diseñar la arquitectura de un agente de inteligencia
artificial capaz de ampliar las funcionalidades del sistema RAG desarrollado
previamente para EcoMarket.

La nueva solución permitirá automatizar el proceso de devolución de productos,
incluyendo la verificación de elegibilidad y la generación de una etiqueta de
devolución.

Para ello se propone una arquitectura basada en:

- LangChain como framework para la construcción del agente.
- El sistema RAG desarrollado en el Taller 2 como herramienta de consulta.
- Herramientas específicas para verificar la elegibilidad de una devolución.
- Una herramienta para generar la etiqueta de devolución.
- Un modelo de lenguaje encargado de decidir qué herramienta debe utilizarse.
