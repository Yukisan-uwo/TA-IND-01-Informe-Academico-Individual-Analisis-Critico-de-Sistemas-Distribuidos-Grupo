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

En la demo, Byron envió un mensaje a un tema de \`#general\`. Codex verificó que seguía visible al volver a abrir el tema. [Captura de la demo](resultados/capturas/zulip-tema-prueba.jpg)

## Fuentes iniciales y su uso

- [How Discord Stores Trillions of Messages, 2023](https://discord.com/blog/how-discord-stores-trillions-of-messages): evidencia técnica de la evolución del almacenamiento, la migración de Cassandra a ScyllaDB y los problemas de rendimiento descritos por Discord.
- [Discord Gateway](https://docs.discord.com/developers/events/gateway): documentación de conexiones y eventos de la API para aplicaciones. Su alcance debe distinguirse de los detalles internos no publicados de los clientes oficiales.
- [Consistency challenges in event-driven microservices, 2026](https://doi.org/10.1007/s00607-026-01701-5): fuente de las fichas de Byron para fundamentar la discusión sobre consistencia y eventos; no demuestra por sí sola decisiones internas de Discord.
- [Impacts of data consistency levels in cloud-based NoSQL for data-intensive applications, 2024](https://doi.org/10.1186/s13677-024-00716-7): fuente de las fichas de Kevin para discutir consistencia y rendimiento. Se revisaron las dos correcciones editoriales; sus implicaciones están en REVISION-FUENTES.md.
- [On the correctness of highly available systems in the presence of failures, 2023](https://doi.org/10.1016/j.jpdc.2023.04.008): candidata de las fichas de Byron para discutir garantías ante fallos. Los datos se contrastaron con la ficha de Elsevier; queda pendiente la apertura personal del DOI por el estudiante.

La bibliografía está en [referencias.bib](informe/referencias.bib). La [revisión de fuentes](informe/REVISION-FUENTES.md) identifica los datos comprobados, las correcciones editoriales y las comprobaciones personales pendientes.

## Experimento realizado

Byron realizó una ronda con Discord web y un teléfono con datos móviles. Al volver la conexión de la laptop, los tres mensajes aparecieron sin recarga manual. El [procedimiento y los resultados](resultados/EXPERIMENTO.md) enlazan las capturas originales y describen lo observado.

## Organización

- `informe/`: fuente LaTeX, bibliografía, revisión de fuentes y [borrador compilado](informe/TA-IND-01-Borrador-Discord-Zulip.pdf). El diagrama digital va en `informe/figuras/`.
- `resultados/`: procedimiento, comandos, transcripción de PowerShell y observaciones. Las capturas originales están en `resultados/capturas/`.
- `evidencias/`: espacios para la foto del bosquejo en `bosquejo/` y las capturas anotadas de artículos en `lecturas/`.
- `entrega/`: espacio para el PDF de una página destinado al SGA.
- [Bitácora](BITACORA.md): registro por fecha de lo realizado, dificultades y tiempo de trabajo.

## Control de la consigna

- [ ] Confirmar la entrega de FORM-FB-01 y FORM-AC-01, y el registro de Discord en el foro.
- [ ] Completar carátula con facultad, paralelo y fecha. Revisar el resumen de 150 a 200 palabras y las cinco páginas de contenido, sin contar carátula, referencias ni anexos.
- [ ] Revisar personalmente introducción, arquitectura, siete transparencias, CAP y PACELC, comunicación, tolerancia a fallos, tabla de comparación, postura crítica y conclusiones.
- [x] Ejecutar una prueba propia y conservar cuatro capturas originales de la laptop y la [transcripción de PowerShell](resultados/sesion-20261112-233908.txt).
- [x] Incorporar dos ejemplos de uso y relacionarlos con conceptos de la unidad. El aviso de reconexión de Discord ilustra la transparencia a fallos y la demo de Zulip ilustra la transparencia de acceso.
- [ ] Incluir la foto original del bosquejo cuando Byron indique que se puede incorporar, y agregar el diagrama final que él elabore a partir del dibujo.
- [x] Incorporar al Anexo B las tres capturas de los fragmentos resaltados por Byron, con página y cita.
- [ ] Abrir cada DOI y comprobar sus datos. Revisar al menos seis fuentes recientes y tres artículos de revistas indexadas.
- [ ] Completar la bitácora con tiempos reales y registrar ocho commits de trabajo con mensajes propios en al menos tres días. Los mensajes redactados por Codex están declarados en la bitácora.
- [ ] Completar la declaración de uso de IA y anotar qué verificó Byron.
- [ ] Grabar de tres a cinco minutos con rostro y voz. Explicar sin leer una captura y la conclusión. Poner el enlace del video en el README y comprobar el acceso.
- [ ] Preparar la defensa oral del método, resultado, límites y cambios posibles.
- [ ] Compilar desde una copia limpia, guardar el PDF del informe en GitHub, comprobar que el repositorio sea público y entregar al SGA el PDF de una página con la URL completa en una sola línea.

## Compilación y video

El borrador está en [main.tex](informe/main.tex). Requiere pdfLaTeX, Biber, babel con español, geometry, graphicx, tabularx, xurl, hyperref, biblatex y el estilo biblatex-ieee. En Windows se usa MiKTeX 25.12 con Biber 2.21. Desde `informe/`, ejecutar:

```text
pdflatex -halt-on-error main.tex
biber main
pdflatex -halt-on-error main.tex
pdflatex -halt-on-error main.tex
```

El PDF generado es un borrador. Queda pendiente añadir el enlace al video.

## Entrega

El trabajo individual se guarda en esta carpeta del repositorio compartido. Al SGA se entrega únicamente un PDF de una página con identificación y la URL completa del repositorio en una sola línea. El cierre es el 15 de noviembre de 2026 a las 23:55, hora de Ecuador.

## Apoyo de IA registrado

Se utilizó Codex para organizar el repositorio, preparar parte del borrador, orientar la revisión bibliográfica y asistir en el piloto. Byron realizó la prueba principal y tomó sus capturas. La declaración en el informe documenta el apoyo y queda pendiente incorporar las verificaciones del estudiante.
