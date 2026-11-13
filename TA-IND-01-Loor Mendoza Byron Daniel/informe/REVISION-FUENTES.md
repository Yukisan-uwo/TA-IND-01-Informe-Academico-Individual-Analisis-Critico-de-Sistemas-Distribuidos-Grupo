# Selección bibliográfica para Discord

Revisión asistida por Codex del 12 de noviembre de 2026. Las fichas iniciales proceden de https://github.com/aldairHub/GHLZ. La selección no sustituye las lecturas y anotaciones personales exigidas por la tarea.

## Artículos reutilizados

1. `bacao2026consistency`, ficha de Byron. La página editorial confirma autores, título, revista Computing, año 2026, volumen 108, artículo 110 y DOI 10.1007/s00607-026-01701-5. Se usará como fundamento de consistencia en sistemas basados en eventos, sin atribuir a Discord las implementaciones descritas por otros sistemas. Lectura propuesta: secciones 2.4 y 6. Fuente: https://link.springer.com/article/10.1007/s00607-026-01701-5.
2. `ferreira2024consistency`, ficha de Kevin. La editorial confirma los cinco autores, título, Journal of Cloud Computing, año 2024, volumen 13, artículo 158 y DOI 10.1186/s13677-024-00716-7. Permite discutir el costo de consistencia en sistemas NoSQL; sus mediciones no son mediciones de Discord. Fuente: https://link.springer.com/article/10.1186/s13677-024-00716-7.
3. `kokocinski2023correctness`, ficha de Byron. La ficha editorial confirma los tres autores, título, Journal of Parallel and Distributed Computing, octubre de 2023, volumen 180, artículo 104707 y DOI 10.1016/j.jpdc.2023.04.008. Servirá para distinguir disponibilidad y garantías ante fallos. La aplicación del modelo a Discord exige justificar sus supuestos. Fuente: https://www.sciencedirect.com/science/article/abs/pii/S0743731523000709. El DOI no abrió directamente mediante la herramienta; la correspondencia se comprobó en la ficha de la editorial y en la lista de publicaciones del autor: https://www.cs.put.poznan.pl/persistentdatastore/papers/index.html.

Los identificadores 110, 158 y 104707 son números de artículo y se guardan como `eid`, no como rangos de páginas. Se conservan los datos comprobados; no se inventan números de fascículo.

## Correcciones del artículo de Ferreira

- El 6 de febrero de 2025 se retiró una afirmación que cuantificaba una reducción del tiempo de respuesta en 4.360 %. No se reutilizará esa cifra. https://doi.org/10.1186/s13677-025-00732-1.
- El 10 de junio de 2025 se corrigió la figura 4. Para comentar esa figura se consultará la versión actualizada, no una copia antigua guardada en las fichas. https://doi.org/10.1186/s13677-025-00754-9.

## Documentación específica

- `ingram2023messages`: publicación de Discord Engineering firmada por Bo Ingram el 6 de marzo de 2023. Respalda la evolución del almacenamiento y las decisiones descritas en esa fecha. No demuestra por sí sola la arquitectura actual completa.
- `discordGateway`: documentación oficial para explicar eventos, conexión WebSocket y recuperación de sesiones de aplicaciones. No permite asumir que observar el cliente web revela todos esos mecanismos internos.
- `smith2023authOutage`: informe de Discord sobre la caída de autenticación del 6 de noviembre de 2023. La pérdida temporal de una zona durante mantenimiento y un disco degradado en otra redujeron la capacidad del clúster. Los reintentos aumentaron la carga y la interrupción impidió leer y enviar mensajes. Las lecturas por cuórum mencionadas en el informe corresponden al clúster de autenticación. [Informe del incidente](https://discord.com/blog/authentication-outage)
- `zulipArchitecture`: describe PostgreSQL para persistencia y el uso de Tornado para entregar eventos mediante peticiones HTTP de larga duración.
- `zulipSendingMessages`: explica el registro del mensaje y sus destinatarios en la base de datos y el envío del evento al sistema de entrega.
- `zulipPostgresql`: documenta un despliegue con PostgreSQL en un servidor separado y la configuración de una réplica de respaldo. Cualquier análisis de recuperación debe indicar qué configuración se considera.

## Verificaciones pendientes antes de entregar

- Confirmar la indexación de Journal of Parallel and Distributed Computing en una fuente oficial. [Computing](https://link.springer.com/journal/607) y [Journal of Cloud Computing](https://link.springer.com/journal/13677/aims-and-scope) declaran SCIE.
- Abrir personalmente cada DOI y contrastar los datos con el artículo, además de esta revisión asistida.
- Revisar la fecha o versión de la documentación viva. La fecha de consulta es distinta de la fecha de publicación.
- Conservar en la bibliografía final únicamente las obras citadas en el texto y compilar con biblatex en estilo IEEE.

La bibliografía contiene once entradas. La selección final depende de las fuentes que se citen y de la comprobación de fechas e indexación.

## Páginas para el Anexo B

1. **Ferreira et al. (2024), página 14 de 16.** El fragmento marcado en *Performance in writing operations* describe el aumento en el tiempo de respuesta y la caída del rendimiento de escritura al pasar de consistencia débil a fuerte. Cita `ferreira2024consistency`, sección CAP y PACELC. [Captura](../evidencias/lecturas/01-ferreira-consistencia.jpg)
2. **Bação y Guerreiro (2026), página 4 de 32.** El fragmento marcado en la sección 2.4, *Event-driven architecture*, describe la publicación y suscripción a eventos para la comunicación asíncrona. Cita `bacao2026consistency`, sección Modelos de comunicación. [Captura](../evidencias/lecturas/02-bacao-eventos.jpg)
3. **Kokociński et al. (2023), página 11 de 18.** El fragmento marcado en la continuación de la sección 6.2, *Replica crashes and phantom operations*, describe una actualización confirmada que se pierde tras el fallo de una réplica. Cita `kokocinski2023correctness`, sección CAP y PACELC. [Captura](../evidencias/lecturas/03-kokocinski-fallos.jpg)

Byron resaltó los fragmentos en los PDF. Codex ubicó las páginas y tomó las capturas en Edge a partir de esos archivos.
