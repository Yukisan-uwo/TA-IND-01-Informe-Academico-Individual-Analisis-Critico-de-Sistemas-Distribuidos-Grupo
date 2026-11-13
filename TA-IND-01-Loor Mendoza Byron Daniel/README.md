# TA-IND-01 - Análisis crítico de Discord

Estudiante: Byron Daniel Loor Mendoza

Asignatura: Aplicaciones Distribuidas

Universidad: Universidad Técnica Estatal de Quevedo

## Estado del trabajo

Sistema principal elegido: Discord. El registro del tema en el foro del SGA está pendiente de confirmar. También está pendiente confirmar la entrega de FORM-FB-01 y FORM-AC-01.

## Alcance del informe

El informe se centrará en el envío, recepción y almacenamiento de mensajes de texto en Discord. Analizará las siete transparencias de distribución indicadas en la guía, CAP y PACELC, los modelos de comunicación y la tolerancia a fallos. Las conclusiones deberán apoyarse en documentación del sistema y resultados observables.

Pregunta de investigación: ¿qué compromisos entre latencia, consistencia y recuperación de fallos aparecen en la entrega y persistencia de mensajes de Discord?

CAP y PACELC se analizarán por componente y operación, según las garantías documentadas. No se atribuirá una clasificación única a toda la plataforma a partir de la base de datos que utiliza. La documentación histórica se identificará por fecha, sin asumir que describe toda la arquitectura actual.

## Comparación con Zulip

La comparación sigue el mismo recorrido en Discord y Zulip: enviar un mensaje de texto, entregarlo en tiempo real y consultarlo en el historial tras una desconexión. En Zulip se estudiará el despliegue documentado con la aplicación y PostgreSQL en servidores distintos. Los criterios son arquitectura, comunicación, transparencias, almacenamiento, consistencia y latencia, y recuperación de fallos.

[Arquitectura de Zulip](https://zulip.readthedocs.io/en/stable/overview/architecture-overview.html) · [Despliegue de PostgreSQL](https://zulip.readthedocs.io/en/stable/production/postgresql.html)

## Fuentes iniciales y su uso

- [How Discord Stores Trillions of Messages, 2023](https://discord.com/blog/how-discord-stores-trillions-of-messages): evidencia técnica de la evolución del almacenamiento, la migración de Cassandra a ScyllaDB y los problemas de rendimiento descritos por Discord.
- [Discord Gateway](https://docs.discord.com/developers/events/gateway): documentación de conexiones y eventos de la API para aplicaciones. Su alcance debe distinguirse de los detalles internos no publicados de los clientes oficiales.
- [Consistency challenges in event-driven microservices, 2026](https://doi.org/10.1007/s00607-026-01701-5): fuente de las fichas de Byron para fundamentar la discusión sobre consistencia y eventos; no demuestra por sí sola decisiones internas de Discord.
- [Impacts of data consistency levels in cloud-based NoSQL for data-intensive applications, 2024](https://doi.org/10.1186/s13677-024-00716-7): fuente de las fichas de Kevin para discutir consistencia y rendimiento. Se revisaron las dos correcciones editoriales; sus implicaciones están en REVISION-FUENTES.md.
- [On the correctness of highly available systems in the presence of failures, 2023](https://doi.org/10.1016/j.jpdc.2023.04.008): candidata de las fichas de Byron para discutir garantías ante fallos. Los datos se contrastaron con la ficha de Elsevier; queda pendiente la apertura personal del DOI por el estudiante.

La bibliografía inicial está en [referencias.bib](referencias.bib). La [revisión de fuentes](REVISION-FUENTES.md) identifica los datos comprobados, las correcciones editoriales y los requisitos todavía pendientes. No constituye aún una bibliografía final validada para entrega.

## Experimento diseñado

El [procedimiento del experimento](EXPERIMENTO.md) registra un piloto en el que Chrome recibió un mensaje mientras DevTools indicaba `Offline`. La prueba principal se hará con Discord web en la laptop y un teléfono con datos móviles. Incluye tres repeticiones, comandos de registro y cuatro capturas previstas. La comparación con Zulip se basa en su documentación técnica.

## Entregables pendientes

- Informe LaTeX con un mínimo de cinco páginas de contenido, resumen de 150 a 200 palabras, declaración de uso de IA y PDF compilado.
- Bibliografía IEEE con biblatex: al menos seis fuentes de los últimos cinco años, incluidas tres de revistas indexadas con DOI verificado. Cada fuente debe citarse donde respalda el análisis.
- Bosquejo de arquitectura dibujado por el estudiante, con nombre y fecha, y diagrama final propio.
- Experimento reproducible con comandos, salidas e interpretación y cuatro capturas originales con datos identificativos visibles.
- Dos ejemplos observados por el estudiante en sistemas de su entorno.
- Tres capturas de lectura de artículos con anotaciones del estudiante, página y correspondencia con citas del informe.
- Bitácora por cada día trabajado e historial de al menos ocho commits en tres días diferentes.
- Video de sustentación de tres a cinco minutos con rostro y voz del estudiante.

## Compilación y video

Se comprobó en Windows la secuencia pdfLaTeX, Biber, pdfLaTeX y pdfLaTeX con MiKTeX 25.12, Biber 2.21 y las nueve entradas de referencias.bib. El documento de prueba usa babel en español y biblatex con estilo IEEE. El archivo principal del informe y el enlace al video se agregarán cuando estén preparados.

## Entrega

El trabajo individual se guarda en esta carpeta del repositorio compartido. Al SGA se entrega únicamente un PDF de una página con identificación y la URL completa del repositorio en una sola línea. El cierre es el 15 de noviembre de 2026 a las 23:55, hora de Ecuador.

## Apoyo de IA registrado

El 12 de noviembre se utilizó Codex para revisar las instrucciones y preparar el README, la bitácora, la selección bibliográfica y el procedimiento experimental. Esto no constituye evidencia de experimentación ni de lectura personal de artículos. La declaración final incorporará el identificador del modelo disponible, los usos posteriores y la verificación efectuada por el estudiante.
