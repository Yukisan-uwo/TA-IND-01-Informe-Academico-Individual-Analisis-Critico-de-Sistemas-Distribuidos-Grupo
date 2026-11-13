# TA-IND-01 — Análisis crítico de RabbitMQ

**Universidad:** Universidad Técnica Estatal de Quevedo  
**Facultad:** Ciencias de la Computación  
**Carrera:** Software  
**Asignatura:** Aplicaciones Distribuidas  
**Actividad:** TA-IND-01 — Informe Académico Individual  
**Estudiante:** Luis Mario Zambrano Párraga  
**Paralelo:** Séptimo nivel, paralelo A

## 1. Descripción

Este repositorio reúne el trabajo realizado para la actividad TA-IND-01, centrado en el análisis crítico de RabbitMQ como sistema distribuido de mensajería.

El estudio aborda la arquitectura del sistema, las transparencias de distribución, los modelos de comunicación, CAP, PACELC y la tolerancia a fallos. También se compara RabbitMQ con Apache Kafka para identificar diferencias y compromisos entre sus diseños.

El análisis combina la revisión de publicaciones científicas con experimentos propios realizados en un clúster local de tres nodos RabbitMQ.

## 2. Objetivo

Analizar el comportamiento de RabbitMQ mediante pruebas de comunicación, replicación, consenso y recuperación ante fallos, para evaluar sus características, limitaciones y compromisos frente a Apache Kafka.

## 3. Organización del repositorio

| Elemento | Contenido |
|---|---|
| `bibliografia/` | Fuentes científicas y registros de lectura |
| `diagramas/` | Bosquejo inicial y diagrama de arquitectura |
| `experimento/` | Configuración, programas, capturas y resultados |
| `informe/` | Informe académico elaborado en LaTeX |
| `BITACORA.md` | Registro de las sesiones de trabajo |
| `README.md` | Presentación y guía general del proyecto |

## 4. Entorno experimental

Las pruebas se desarrollaron en Windows utilizando Docker Desktop y RabbitMQ 4.2.9 sobre Erlang 27.3.4.19.

Se configuró un clúster de tres nodos y una cola de quórum denominada `taind01_mensajes`. Para la comunicación desde aplicaciones Python 3.11.9 se utilizó Pika 1.4.4.

Los tres nodos se ejecutaron en contenedores sobre una misma computadora, por lo que las pruebas representan fallos de nodos individuales, no de servidores físicos independientes.

## 5. Resumen de experimentos

| Prueba | Resultado observado |
|---|---|
| Formación del clúster | Tres nodos integrados correctamente |
| Creación de cola de quórum | Tres miembros con replicación mediante Raft |
| Mensajería desde el panel web | Tres mensajes publicados y recuperados |
| Mensajería mediante Python | Cinco mensajes publicados y consumidos con confirmaciones |
| Caída del líder | `rabbit3` asumió el liderazgo y se conservaron los cinco mensajes |
| Reincorporación | El nodo detenido regresó y sincronizó su estado |
| Pérdida de mayoría | Con un solo miembro activo no se observó un líder operativo |
| Recuperación del quórum | Se conservaron y recuperaron cinco mensajes |
| Sincronización final | Las tres réplicas alcanzaron el índice de confirmación 70 |

Las pruebas permitieron estudiar el comportamiento de la mensajería replicada ante fallos de contenedores. No se realizaron pruebas de partición de red real ni mediciones comparativas de latencia.

**Documentación técnica:** [Procedimientos y resultados de los experimentos](experimento/README-Experimento.md).

## 6. Informe académico

El informe se desarrollará en LaTeX e incluirá:

- Arquitectura y transparencias de distribución.
- Análisis de CAP y PACELC.
- Modelos de comunicación y tolerancia a fallos.
- Interpretación de los experimentos realizados.
- Comparación crítica entre RabbitMQ y Apache Kafka.
- Conclusiones sustentadas en resultados y bibliografía.

### Compilación

El informe utilizará `biblatex` con estilo IEEE y el sistema de procesamiento bibliográfico `biber`.

La secuencia de compilación prevista es:

```text
pdflatex → biber → pdflatex → pdflatex
```

**Pendiente de completar:** nombre y ruta del archivo principal, comandos exactos, dependencias de LaTeX y comprobación de que el PDF se regenera correctamente desde el repositorio.

## 7. Evidencias de autoría

Se conservan capturas originales de la ejecución de RabbitMQ, archivos de configuración, programas Python y resultados de las pruebas.

El repositorio también contiene la bitácora de trabajo y el bosquejo inicial de la arquitectura elaborado a mano.

Las capturas de lectura científica, el diagrama definitivo y los demás anexos se incorporarán conforme avance el informe.

## 8. Sustentación

**Video de sustentación:** pendiente de incorporación.

El enlace al video de 3 a 5 minutos se publicará en este apartado una vez completada la grabación.

## 9. Estado del proyecto

**Completado:** preparación del entorno, formación del clúster y pruebas de mensajería, replicación, caída del líder, pérdida de mayoría y recuperación.

**Pendiente:** revisión bibliográfica, análisis crítico comparativo, diagrama definitivo, informe LaTeX, capturas de lectura y video de sustentación.
