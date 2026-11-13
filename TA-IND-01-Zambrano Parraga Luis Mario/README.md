# TA-IND-01 - Análisis crítico de RabbitMQ

**Universidad:** Universidad Técnica Estatal de Quevedo  
**Facultad:** Ciencias de la Computación  
**Carrera:** Software  
**Asignatura:** Aplicaciones Distribuidas  
**Actividad:** TA-IND-01 - Informe Académico Individual  
**Estudiante:** Luis Mario Zambrano Párraga

## 1. Descripción del proyecto

Este repositorio contiene el desarrollo de la actividad TA-IND-01, centrada en el análisis crítico de RabbitMQ como sistema distribuido de mensajería.

El trabajo estudia su arquitectura, las transparencias de distribución, el teorema CAP y su extensión PACELC, los modelos de comunicación y la tolerancia a fallos. También se considera Apache Kafka como sistema de comparación.

El análisis combina investigación bibliográfica con pruebas realizadas en un entorno local de Docker.

## 2. Objetivo

Analizar el funcionamiento de RabbitMQ en un entorno distribuido, mediante pruebas de comunicación, replicación y tolerancia a fallos, para identificar sus características, ventajas y limitaciones frente a Apache Kafka.

## 3. Organización del repositorio

- **bibliografia/**: referencias científicas y registros de lectura.
- **diagramas/**: bosquejo inicial de la arquitectura y diagrama definitivo.
- **experimento/**: configuración de RabbitMQ, programas Python, capturas y resultados.
- **informe/**: documentos LaTeX y PDF del informe académico.
- **BITACORA.md**: registro de actividades, dificultades, soluciones y tiempo dedicado.
- **README.md**: descripción del proyecto e instrucciones para reproducir las pruebas.

## 4. Entorno experimental

Para las pruebas se utiliza la siguiente configuración:

| Componente | Versión o configuración |
|---|---|
| Sistema operativo | Windows |
| Contenedores | Docker Desktop |
| RabbitMQ | 4.2.9 |
| Erlang | 27.3.4.19 |
| Nodos RabbitMQ | 3 |
| Tipo de cola | Quorum |
| Cola utilizada | taind01_mensajes |
| Cliente de mensajería | Python 3.11.9 |
| Biblioteca AMQP | Pika 1.4.4 |

El entorno contiene tres contenedores RabbitMQ conectados en un clúster. Las pruebas utilizan una cola de quórum distribuida entre sus tres nodos.

Todos los contenedores se ejecutan en una misma computadora, por lo que el entorno permite estudiar fallos individuales de contenedores, pero no representa tres servidores físicos independientes.

## 5. Pruebas realizadas

### 5.1. Inicialización del entorno

Se configuraron tres contenedores RabbitMQ mediante Docker Compose y se verificó su funcionamiento desde PowerShell.

### 5.2. Formación del clúster

Se incorporaron los nodos `rabbit@rabbit2` y `rabbit@rabbit3` al clúster iniciado por `rabbit@rabbit1`.

El comando `rabbitmqctl cluster_status` permitió comprobar que los tres nodos estaban activos y que no se reportaban particiones de red.

### 5.3. Creación de una cola de quórum

Se creó la cola `taind01_mensajes`, de tipo Quorum, y se consultó su estado para identificar los miembros y el líder.

### 5.4. Publicación y consumo desde RabbitMQ Management

Se publicaron tres mensajes desde la interfaz web.

Antes del consumo se observaron tres mensajes pendientes y ninguno sin confirmar. Después de recuperarlos con confirmación automática, la cola quedó vacía.

### 5.5. Publicación y consumo mediante Python

Se desarrollaron dos programas utilizando la biblioteca Pika:

- `productor.py`: publica cinco mensajes persistentes utilizando confirmaciones del broker.
- `consumidor.py`: recupera los mensajes y envía confirmaciones manuales mediante `basic_ack()`.

El productor obtuvo confirmaciones de cinco publicaciones. Posteriormente, el consumidor recuperó los cinco mensajes y la consulta final mostró cero mensajes pendientes y cero sin confirmar.

Los registros y las capturas se encuentran en `experimento/resultados/` y `experimento/capturas/`.

## 6. Reproducción de las pruebas

### 6.1. Requisitos

- Docker Desktop con soporte para contenedores Linux.
- Docker Compose.
- Python 3.11.
- Biblioteca Pika, indicada en `requirements.txt`.

### 6.2. Inicializar RabbitMQ

Desde la carpeta `experimento/`, validar la configuración y crear los contenedores:

1. `docker compose config -q`
2. `docker compose up -d`
3. `docker compose ps`

Para comprobar que el primer nodo responde:

`docker compose exec rabbit1 rabbitmq-diagnostics -q ping`

### 6.3. Formar el clúster

En una instalación nueva, con los tres nodos iniciados y sin datos previos, ejecutar:

1. `docker compose exec rabbit2 rabbitmqctl join_cluster rabbit@rabbit1`
2. `docker compose exec rabbit3 rabbitmqctl join_cluster rabbit@rabbit1`

Verificar el resultado:

`docker compose exec rabbit1 rabbitmqctl cluster_status`

Estos comandos de unión no deben repetirse innecesariamente si el clúster ya está formado.

### 6.4. Crear la cola

Ingresar a RabbitMQ Management mediante `http://localhost:15672`.

Utilizar las credenciales de laboratorio definidas en la configuración local y crear una cola con estas características:

- Nombre: `taind01_mensajes`
- Tipo: `Quorum`
- Virtual host: `/`
- Tamaño inicial del grupo: predeterminado (tres miembros en este entorno).

Consultar su estado mediante:

`docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes`

### 6.5. Ejecutar los programas Python

Instalar las dependencias desde `experimento/`:

`python -m pip install -r requirements.txt`

Configurar en PowerShell la variable de entorno `RABBITMQ_PASSWORD` con la contraseña del laboratorio definida en Docker Compose.

Ejecutar el productor:

`python productor.py`

Consultar los mensajes pendientes:

`docker compose exec rabbit1 rabbitmqctl list_queues name type messages_ready messages_unacknowledged`

Ejecutar el consumidor:

`python consumidor.py`

Volver a consultar la cola para verificar el resultado.

Los programas se ejecutan desde la carpeta `experimento/` y se conectan al primer nodo mediante `127.0.0.1:5672`.

## 7. Evidencias de autoría

El repositorio conserva evidencias obtenidas durante el desarrollo:

- Capturas del funcionamiento de los contenedores.
- Resultados de la formación del clúster.
- Capturas de la cola de quórum y sus miembros.
- Publicación y recuperación de mensajes desde la interfaz web.
- Ejecución de los programas Python.
- Registros de comandos y resultados obtenidos.
- Bosquejo de arquitectura dibujado a mano.
- Bitácora de las sesiones de trabajo.

Los resultados se documentan con base en las observaciones efectuadas durante las pruebas.

## 8. Informe académico y compilación

El informe se desarrollará en LaTeX, utilizando `biblatex` con estilo IEEE para gestionar las referencias bibliográficas.

La compilación prevista utilizará `pdflatex` y `biber`, en el siguiente orden:

1. `pdflatex`
2. `biber`
3. `pdflatex`
4. `pdflatex`

**Pendiente:** Todavia no estoy en esta fase.

## 9. Sustentación

**Video de sustentación:** pendiente de incorporación.

Se agregará aquí el enlace al video una vez realizada la sustentación.

## 10. Estado actual

Se completaron las pruebas iniciales de configuración del clúster, creación de la cola y comunicación mediante la interfaz web y programas Python.

**Actividades pendientes:** experimentos de tolerancia a fallos y recuperación, análisis bibliográfico y comparativo, elaboración del diagrama definitivo, informe LaTeX y video de sustentación.
