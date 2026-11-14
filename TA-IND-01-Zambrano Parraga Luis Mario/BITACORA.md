# Bitácora de trabajo - TA-IND-01

## 11 de noviembre de 2026

**Actividades realizadas:**
- Selección y registro de RabbitMQ en el grupo de whashapp de mis compañeros.
- Creación del repositorio de GitHub.
- Elaboración del README inicial.

**Dificultades encontradas:**
Decidir cual sistema escoger, como fui el primero en apartar mi sistema para que no se repitan
**Soluciones aplicadas:**
Entonces comparé los sistemas y escogí el que me interesara más, a la final escogi RabbitMQ y lo compararé con Apache Apache Kafka, es lo que he pensado hasta ahora.

**Tiempo dedicado:**
2 horas


## 12 de noviembre de 2026

### Actividades realizadas
- Preparé el entorno experimental de RabbitMQ utilizando Docker Desktop.
- Configuré tres contenedores con RabbitMQ 4.2.9 mediante Docker Compose.
- Comprobé el funcionamiento de los contenedores y la respuesta del primer nodo.
- Uní los nodos `rabbit2` y `rabbit3` al clúster principal.
- Verifiqué el estado del clúster mediante el comando `rabbitmqctl cluster_status`.
- Revisé los tres nodos desde el panel de administración de RabbitMQ.
- Creé la cola de quórum `taind01_mensajes` y realicé consultas para comprobar sus miembros.
- Guardé capturas de las pruebas y los registros obtenidos desde la terminal.
- Elaboré a mano el primer bosquejo de la arquitectura experimental, identificando los nodos de RabbitMQ y sus componentes principales.

### Problemas encontrados
Al intentar iniciar los contenedores, Docker no podía conectarse al motor de contenedores Linux porque Docker Desktop todavía no estaba abierto.

### Solución aplicada
Abrí Docker Desktop y volví a ejecutar `docker compose up -d`. Los tres contenedores iniciaron correctamente y pude continuar con la configuración del clúster.

### Resultados obtenidos
- Se inició un entorno de tres contenedores RabbitMQ.
- Los tres nodos quedaron registrados como activos dentro del mismo clúster.
- La consulta `cluster_status` no mostró alarmas ni particiones de red.
- Se crearon registros y capturas para respaldar las pruebas realizadas.
- Se obtuvo el bosquejo de arquitectura que servirá como base para elaborar el diagrama definitivo.

### Evidencias generadas
- `experimento/docker-compose.yml`
- `experimento/capturas/01-contenedores-iniciales.png` hasta `06-miembros-quorum.png`
- `experimento/resultados/02-estado-cluster.txt`
- `experimento/resultados/03-estado-cola-quorum.txt`
- `diagramas/boceto-inicial.jpeg`

### Tiempo dedicado
Aproximadamente 2 horas y 30 minutos.

### Continuación de otro commit: pruebas de mensajería

**Actividades realizadas:**
- Publiqué tres mensajes desde el panel de administración de RabbitMQ.
- Comprobé que los mensajes permanecían pendientes sin consumidores conectados.
- Recuperé los mensajes utilizando la opción de confirmación automática.
- Preparé un productor Python con la biblioteca Pika y confirmaciones de publicación.
- Envié cinco mensajes desde Python y comprobé que quedaron pendientes en la cola.
- Preparé un consumidor Python con confirmaciones manuales.
- Recuperé los cinco mensajes y comprobé que la cola quedó vacía.
- Guardé capturas y registros de los resultados.

**Resultados:**
- Se publicaron y recuperaron tres mensajes desde RabbitMQ Management.
- El productor Python obtuvo confirmaciones de cinco publicaciones.
- El consumidor Python procesó cinco mensajes y envió sus confirmaciones manuales.
- La consulta final mostró cero mensajes pendientes y cero sin confirmar.

**Dificultades:** no tuve dificultades esta vez.

**Tiempo adicional dedicado:** 1 hora.


## 13 de noviembre de 2026

### Actividades realizadas

- Continué las pruebas de tolerancia a fallos del clúster RabbitMQ.
- Modifiqué el consumidor Python para permitir la conexión a distintos nodos mediante la variable `RABBITMQ_PORT`.
- Recuperé cinco mensajes desde `rabbit2` mientras `rabbit1` permanecía detenido.
- Reinicié `rabbit1` y comprobé su reincorporación a la cola de quórum.
- Realicé una prueba de pérdida de mayoría, deteniendo primero `rabbit2` y después `rabbit3`.
- Consulté el estado de Raft cuando solamente quedó un nodo activo.
- Reinicié `rabbit3` para restablecer la mayoría.
- Comprobé que los cinco mensajes permanecían pendientes después de la recuperación.
- Consumí los cinco mensajes y reinicié `rabbit2`.
- Verifiqué nuevamente los índices de las tres réplicas.

### Problemas y comportamientos observados

Al detener dos de los tres nodos, la cola perdió la mayoría necesaria para elegir un líder operativo. El nodo restante apareció en estado `pre_vote`.

### Solución y recuperación

Reinicié `rabbit3` sin eliminar los volúmenes ni restablecer la configuración. El clúster recuperó la mayoría y volvió a mostrar un líder operativo. Posteriormente inicié `rabbit2` para completar la recuperación.

### Resultados obtenidos

- La cola continuó disponible después de la primera caída del líder.
- Los cinco mensajes publicados antes de ese fallo pudieron consumirse desde otro nodo.
- Con dos nodos detenidos, no existía un líder operativo para la cola de quórum.
- Al recuperar la mayoría, se conservaron los cinco mensajes pendientes.
- Los cinco mensajes fueron procesados con confirmaciones manuales.
- Después de reincorporar todos los nodos, las tres réplicas alcanzaron el índice de confirmación 70.

### Evidencias

Se conservaron las capturas y los registros de las pruebas de tolerancia a fallos, pérdida de mayoría, recuperación y sincronización en `experimento/capturas/` y `experimento/resultados/`.

### Tiempo dedicado

2 horas y 40 minutos aproximadamente

## Continuación de la sesión — revisión de fuentes y estructura del informe (13 de noviembre de 2026)

### Actividades realizadas:
- Revisé artículos científicos sobre arquitectura y mensajería de RabbitMQ, CAP, PACELC, Raft, transparencias y comparación con Kafka.
- Localicé y resalté fragmentos en las publicaciones originales; añadí anotaciones relacionándolos con los apartados del informe.
- Preparé nueve capturas de lectura y corregí las que necesitaban un mejor resaltado o mostrar la página.
- Revisé una plantilla LaTeX compartida como referencia de formato y adapté su estructura a mi tema de RabbitMQ, sin reutilizar el contenido ajeno.
- Organicé main.tex y referencias.bib en la carpeta informe/ y comprobé las citas y los comandos de compilación con apoyo de ChatGPT.

### Dificultades encontradas: 
Algunos artículos están en inglés y costó localizar los fragmentos relevantes. También fue necesario revisar las rutas de las figuras y de la bibliografía según la estructura de carpetas del repositorio.

### Cómo las resolví: 
Consulté las traducciones como apoyo, contrasté los fragmentos con los PDF originales y corregí las rutas de LaTeX para que main.tex y referencias.bib estén juntos. Dejé identificados los apartados que aún no están completos.

### Resultado de la sesión: 
Nueve capturas de lectura preparadas, siete fuentes utilizadas en el borrador del informe y estructura LaTeX compilable. Todavía faltan datos de portada, diagrama definitivo, ejemplos personales, incidente documentado y revisión final del PDF con todas las evidencias.

### Tiempo dedicado:
4 horas aproximadamente.

## Cierre del informe, diagrama y sustentación (13 de noviembre de 2026)
### Actividades realizadas
- Completé la redacción del informe sobre RabbitMQ y su comparación crítica con Apache Kafka.
- Organicé los apartados de arquitectura, transparencias de distribución, CAP, PACELC, modelos de comunicación, tolerancia a fallos y recuperación.
- Incorporé la descripción de las pruebas realizadas, sus resultados y las limitaciones del entorno experimental.
- Añadí ejemplos relacionados con el SGA de la UTEQ y el uso de GitHub, diferenciando las observaciones personales de las características internas que no fueron verificadas.
- Incluí un incidente real documentado como referencia para relacionar la disponibilidad del servicio con las condiciones de infraestructura.
- Revisé las referencias bibliográficas y las citas del documento, utilizando biblatex con estilo IEEE y Biber.
- Incorporé al informe las capturas de las pruebas experimentales y las nueve capturas anotadas de lectura como evidencias.
- Elaboré el diagrama definitivo de la arquitectura en draw.io y guardé tanto el archivo XML editable como sus exportaciones PNG.
- Conservé el bosquejo inicial elaborado a mano para incluirlo como evidencia del proceso.
- Revisé la presentación del PDF y comparé su organización visual con un ejemplo de informe de otro estudiante, utilizando únicamente el formato como referencia.
- Revisé errores reportados durante la compilación de main.tex y referencias.bib y realicé las correcciones correspondientes.
- Revisé la sincronización del repositorio. Ejecuté git fetch origin, git pull --rebase origin main y git push origin main; posteriormente comprobé que la rama local estuviera actualizada con origin/main.
- Dejé fuera del control de versiones los archivos auxiliares generados por LaTeX, como .aux, .bcf, .blg, .log, .out y .run.xml, conservando los archivos fuente y el PDF de entrega.
- Preparé el guion, grabé el video de sustentación y lo publiqué en YouTube.
### Dificultades encontradas
- Durante la compilación aparecieron errores relacionados con el documento LaTeX y las referencias bibliográficas.
- Al sincronizar GitHub, la rama local y la remota llegaron a tener cambios distintos, por lo que inicialmente no se podían enviar los cambios directamente.
- Se generaron archivos auxiliares de LaTeX que no correspondían a los archivos finales que se debían subir al repositorio.
### Soluciones aplicadas
- Revisé las líneas señaladas en main.tex y referencias.bib y corregí los elementos que estaban provocando los errores reportados.
- Sincronicé los cambios remotos con git fetch y git pull --rebase antes de ejecutar nuevamente git push.
- Comprobé el estado de Git y decidí no agregar los archivos auxiliares de compilación a la entrega.
- Organicé el diagrama con su archivo editable y sus exportaciones para conservar la posibilidad de modificarlo posteriormente.
### Resultados obtenidos
- Informe académico desarrollado en LaTeX, con bibliografía y evidencias.
- PDF del informe generado para su revisión y entrega.
- Diagrama de arquitectura elaborado en draw.io, con XML editable y archivos PNG.
- Capturas de lectura y de experimentación organizadas en sus respectivas carpetas.
- Repositorio sincronizado con la rama remota.
- Video de sustentación publicado en YouTube: https://youtu.be/QhIJK3b6n10
### Observación para la revisión final
Al revisar nuevamente los archivos publicados, se identificó que algunos nombres de imágenes del repositorio deben coincidir exactamente con las rutas indicadas en main.tex. Por ello, antes de considerar reproducible la compilación desde una copia limpia del repositorio, se debe verificar esa correspondencia y volver a generar el PDF.
### Tiempo dedicado
3 horas aproximadamente.
