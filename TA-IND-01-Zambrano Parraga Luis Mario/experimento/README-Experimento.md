# Experimentación con RabbitMQ

## 1. Descripción

Este directorio contiene las configuraciones, programas y evidencias de los experimentos realizados sobre RabbitMQ para la actividad TA-IND-01.

Las pruebas se realizaron sobre un clúster local de tres nodos y una cola de quórum. Se estudiaron la comunicación asíncrona, la replicación, las confirmaciones de mensajes, la elección de líderes, la tolerancia a fallos y la recuperación del servicio.

Los procedimientos se presentan en el orden en que deben ejecutarse. Las pruebas de caída de nodos están destinadas exclusivamente a un entorno de laboratorio.

## 2. Requisitos del entorno

| Componente | Configuración |
|---|---|
| Sistema operativo | Windows |
| Contenedores | Docker Desktop con motor Linux |
| RabbitMQ | 4.2.9-management |
| Erlang | 27.3.4.19 |
| Python | 3.11.9 |
| Biblioteca Python | Pika 1.4.4 |
| Nodos | rabbit1, rabbit2, rabbit3 |
| Cola | taind01_mensajes |
| Tipo de cola | Quorum |
| Protocolo del cliente | AMQP 0-9-1 |

Los tres contenedores comparten la computadora anfitriona, pero disponen de procesos y almacenamiento persistente independientes.

## 3. Archivos del experimento

| Archivo o carpeta | Descripción |
|---|---|
| `docker-compose.yml` | Configuración de los tres contenedores |
| `productor.py` | Publicación de cinco mensajes con confirmaciones |
| `consumidor.py` | Consumo de mensajes con ACK manual |
| `requirements.txt` | Dependencias de Python |
| `capturas/` | Evidencias visuales originales |
| `resultados/` | Salidas obtenidas durante las pruebas |

Los comandos siguientes deben ejecutarse en PowerShell desde la carpeta `experimento/`, donde se encuentran los archivos de configuración y los programas Python.

## 4. Preparación del clúster

### 4.1. Inicialización

Con Docker Desktop funcionando, validar la configuración:

```powershell
docker compose config -q
```

Iniciar los contenedores:

```powershell
docker compose up -d
docker compose ps
```

Comprobar la respuesta del primer nodo:

```powershell
docker compose exec rabbit1 rabbitmq-diagnostics -q ping
```

**Resultado observado:** los tres contenedores iniciaron y la comprobación del primer nodo devolvió `Ping succeeded`.

### 4.2. Formación del clúster

Para una instalación nueva, con nodos independientes y sin datos anteriores, ejecutar:

```powershell
docker compose exec rabbit2 rabbitmqctl join_cluster rabbit@rabbit1
docker compose exec rabbit3 rabbitmqctl join_cluster rabbit@rabbit1
```

Verificar la integración:

```powershell
docker compose exec rabbit1 rabbitmqctl cluster_status
```

**Resultado observado:** los nodos `rabbit@rabbit1`, `rabbit@rabbit2` y `rabbit@rabbit3` aparecieron en `Running Nodes`, sin alarmas ni particiones de red.

**Precaución:** `join_cluster` debe utilizarse durante la formación inicial. No debe repetirse para reincorporar nodos que ya pertenecen al clúster, porque una unión a otro clúster puede descartar datos previos.

## 5. Creación y verificación de la cola

### 5.1. Creación mediante RabbitMQ Management

Ingresar a:

`http://localhost:15672`

Utilizar las credenciales de laboratorio definidas en `docker-compose.yml`.

En **Queues and Streams → Add a new queue**, seleccionar:

| Campo | Valor |
|---|---|
| Type | Quorum |
| Virtual host | / |
| Name | taind01_mensajes |
| Node | rabbit@rabbit1 |
| Arguments | Predeterminados |

Crear la cola mediante **Add queue**.

La cola de quórum se distribuyó entre los tres nodos disponibles.

### 5.2. Verificación

Comprobar el tipo:

```powershell
docker compose exec rabbit1 rabbitmqctl list_queues name type durable
```

Consultar el estado de sus miembros:

```powershell
docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

**Resultado observado:** cola `quorum`, duradera, con tres miembros y un líder.

La existencia de tres nodos en un clúster no implica por sí sola que cualquier cola esté replicada. Por ese motivo se verificó específicamente el tipo y los miembros de `taind01_mensajes`.

## 6. Pruebas de mensajería

### 6.1. Publicación desde RabbitMQ Management

Desde los detalles de `taind01_mensajes`, utilizar **Publish message** para enviar tres mensajes de prueba identificados como 001, 002 y 003.

Posteriormente comprobar:

```powershell
docker compose exec rabbit1 rabbitmqctl list_queues name type messages_ready messages_unacknowledged
```

**Resultado observado:**

- Mensajes pendientes: 3.
- Mensajes sin confirmar: 0.
- Consumidores conectados: 0.

Los mensajes permanecieron en la cola sin un consumidor activo.

### 6.2. Consumo desde RabbitMQ Management

En **Get messages**, configurar tres mensajes y `Automatic ack`.

Después de recuperarlos se volvió a consultar el estado de la cola.

**Resultado observado:** se recuperaron los tres mensajes y la cola quedó con cero mensajes pendientes y cero sin confirmar.

### 6.3. Preparación de Python

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

Configurar la contraseña del laboratorio mediante la variable de entorno `RABBITMQ_PASSWORD`.

En PowerShell:

```powershell
$env:RABBITMQ_PASSWORD = Read-Host "Contrasena de laboratorio"
```

El valor debe coincidir con la contraseña configurada en RabbitMQ. No es necesario guardarla en los scripts ni en los registros públicos.

### 6.4. Publicación desde Python

Ejecutar:

```powershell
python productor.py
```

El programa se conecta a `127.0.0.1:5672`, comprueba la existencia de la cola, activa `confirm_delivery()` y publica cinco mensajes persistentes con identificadores individuales.

Consultar los mensajes:

```powershell
docker compose exec rabbit1 rabbitmqctl list_queues name type messages_ready messages_unacknowledged
```

**Resultado observado:** cinco publicaciones confirmadas por RabbitMQ y cinco mensajes pendientes de consumo.

### 6.5. Consumo desde Python

Ejecutar:

```powershell
python consumidor.py
```

El consumidor utiliza `basic_get(auto_ack=False)` para recuperar los mensajes y `basic_ack()` para confirmarlos manualmente.

**Resultado observado:** cinco mensajes recuperados, cinco confirmaciones manuales enviadas y cero mensajes pendientes en la consulta posterior.

Los programas permiten estudiar las confirmaciones del productor y del consumidor como mecanismos diferentes.

## 7. Prueba de caída del líder

**Objetivo:** observar el comportamiento de la cola cuando se detiene uno de sus tres miembros, concretamente el líder.

### 7.1. Estado inicial

Con los tres nodos activos y la cola vacía, consultar:

```powershell
docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

En la ejecución original el líder era `rabbit@rabbit1`. En una reproducción debe comprobarse el líder actual antes de detenerlo, porque puede ser diferente.

Publicar cinco mensajes:

```powershell
python productor.py
```

Comprobar que estén pendientes:

```powershell
docker compose exec rabbit1 rabbitmqctl list_queues name type messages_ready messages_unacknowledged
```

### 7.2. Detención del líder

En la ejecución original se utilizó:

```powershell
docker compose stop rabbit1
docker compose ps
```

Consultar desde otro miembro:

```powershell
docker compose exec rabbit2 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

**Resultado observado:**

- `rabbit1` quedó detenido.
- `rabbit2` permaneció como seguidor.
- `rabbit3` asumió el liderazgo.
- Los cinco mensajes continuaron pendientes.

### 7.3. Consumo durante el fallo

El consumidor admite seleccionar el puerto mediante `RABBITMQ_PORT`.

Se utilizó el puerto de `rabbit2`:

```powershell
$env:RABBITMQ_PORT = "5673"
python consumidor.py
```

**Resultado observado:** los cinco mensajes se recuperaron y confirmaron mientras `rabbit1` continuaba detenido.

La prueba demostró que la cola pudo seguir atendiendo operaciones con dos de sus tres miembros disponibles.

### 7.4. Reincorporación

Reiniciar el nodo:

```powershell
docker compose start rabbit1
```

Comprobar el clúster y la cola:

```powershell
docker compose exec rabbit2 rabbitmqctl cluster_status
docker compose exec rabbit2 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

**Resultado observado:** `rabbit1` regresó como seguidor y las tres réplicas alcanzaron el índice de confirmación 51.

No fue necesario repetir `join_cluster`.

## 8. Prueba de pérdida de mayoría

**Objetivo:** analizar qué ocurre cuando una cola de quórum de tres miembros pierde dos nodos.

### 8.1. Preparación

Con los tres miembros recuperados, verificar su estado:

```powershell
docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

Publicar cinco mensajes nuevos:

```powershell
python productor.py
```

Comprobar que estén pendientes:

```powershell
docker compose exec rabbit1 rabbitmqctl list_queues name type messages_ready messages_unacknowledged
```

### 8.2. Primera detención

Detener `rabbit2`:

```powershell
docker compose stop rabbit2
docker compose ps -a
```

Consultar la cola:

```powershell
docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

**Resultado observado:** `rabbit1` y `rabbit3` permanecieron activos, con `rabbit3` como líder y el índice de confirmación 58.

### 8.3. Segunda detención

Detener `rabbit3`:

```powershell
docker compose stop rabbit3
docker compose ps -a
```

Consultar desde el único nodo restante:

```powershell
docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

**Resultado observado:** `rabbit1` apareció en estado `pre_vote`, mientras `rabbit2` y `rabbit3` figuraban como `nodedown`.

No existía un líder operativo porque únicamente quedaba disponible uno de los tres votantes.

Esta prueba no incluyó una medición de latencia ni una solicitud de publicación durante la pérdida de mayoría. Tampoco constituye una simulación de partición de red.

## 9. Recuperación del quórum

### 9.1. Restablecimiento de mayoría

Con `rabbit1` activo y los otros dos nodos detenidos, se reinició `rabbit3`:

```powershell
docker compose start rabbit3
docker compose ps -a
```

Consultar:

```powershell
docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

**Resultado observado:** `rabbit3` volvió a actuar como líder. Los miembros disponibles alcanzaron el índice de confirmación 59.

### 9.2. Comprobación de mensajes

Ejecutar:

```powershell
docker compose exec rabbit1 rabbitmqctl list_queues name type messages_ready messages_unacknowledged
```

**Resultado observado:** los cinco mensajes continuaban pendientes después de restablecer la mayoría.

### 9.3. Recuperación mediante Python

Configurar el consumidor para conectarse a `rabbit1`:

```powershell
$env:RABBITMQ_PORT = "5672"
python consumidor.py
```

Consultar el estado posterior:

```powershell
docker compose exec rabbit1 rabbitmqctl list_queues name type messages_ready messages_unacknowledged
```

**Resultado observado:** los cinco mensajes fueron recuperados y confirmados. La cola terminó sin mensajes pendientes.

### 9.4. Recuperación completa del clúster

Iniciar el miembro restante:

```powershell
docker compose start rabbit2
docker compose ps -a
```

Comprobar el estado:

```powershell
docker compose exec rabbit1 rabbitmq-queues quorum_status --vhost / taind01_mensajes
```

**Resultado observado:** las tres réplicas quedaron activas, con índices de registro, escritura, aplicación y confirmación iguales a 70. `rabbit3` continuó como líder.

## 10. Evidencias y resultados originales

Las capturas se encuentran en `capturas/` y los registros de texto en `resultados/`.

| Capturas | Experimentos documentados |
|---|---|
| 01–06 | Contenedores, formación del clúster y cola de quórum |
| 07–08 | Publicación y consumo desde el panel web |
| 09–12 | Productor y consumidor Python |
| 13–19 | Caída del líder, conservación de mensajes y reincorporación |
| 20–23 | Pérdida progresiva de la mayoría |
| 24–27 | Recuperación del quórum, consumo y sincronización final |

Los archivos de `resultados/` conservan las salidas originales de los comandos ejecutados durante las pruebas, incluyendo el estado de la cola, los miembros de Raft y las operaciones de publicación y consumo.

Para repetir una consulta y guardar su salida se puede utilizar PowerShell con `Tee-Object`. Ejemplo:

```powershell
docker compose exec -T rabbit1 rabbitmqctl cluster_status | Tee-Object -FilePath ".\resultados\estado-cluster-repeticion.txt"
```

El archivo generado en una repetición debe distinguirse de los resultados históricos de las pruebas originales.

Las capturas originales incluyen datos de identificación del entorno de trabajo, fecha y hora, conforme a las evidencias de autoría requeridas.

## 11. Problemas encontrados

### Motor de Docker no iniciado

En el primer intento, `docker compose up -d` no pudo conectarse al motor Linux de Docker.

Se abrió Docker Desktop y posteriormente los tres contenedores iniciaron correctamente.

### Comando `py` no disponible

Windows no reconoció el lanzador `py`. Se comprobó que Python 3.11.9 sí estaba disponible mediante `python`, por lo que se utilizó ese comando sin reinstalar el intérprete.

### Cambio de nodo para el consumidor

Al detener `rabbit1`, el consumidor no podía utilizar el puerto original `5672`. Se adaptó el programa para leer `RABBITMQ_PORT` y se estableció `5673` para conectarse a `rabbit2`.

## 12. Precauciones y limitaciones

- Las pruebas de fallo deben ejecutarse únicamente sobre el clúster de laboratorio.
- Antes de detener un líder, se debe comprobar su identidad actual.
- Los comandos están organizados secuencialmente; algunos requieren que la cola esté vacía o que existan cinco mensajes pendientes.
- No utilizar `docker compose down -v`, porque eliminaría los volúmenes de datos.
- No ejecutar `reset` ni repetir `join_cluster` durante las pruebas de recuperación.
- Las credenciales incluidas en la configuración se utilizan exclusivamente para el laboratorio local y no deben reutilizarse en producción.
- Los tres nodos comparten una sola computadora física.
- Se comprobaron caídas de contenedores, no particiones de red auténticas.
- No se midió el tiempo de elección de líder ni la latencia de las operaciones.
- La recepción confirmada de cinco mensajes no demuestra entrega exactamente una vez en todos los escenarios posibles.

Las conclusiones de este experimento deben interpretarse dentro de estas condiciones.

## 13. Conclusión experimental

Las pruebas mostraron que una cola de quórum con tres miembros pudo continuar funcionando después de la caída de uno de ellos, conservar mensajes previamente confirmados y permitir su recuperación mediante otro nodo.

También se observó que, al detener dos miembros, el nodo restante no consiguió establecer un líder operativo. Al recuperar la mayoría, los mensajes pendientes continuaron disponibles y pudieron consumirse.

Finalmente, los tres miembros se reincorporaron y alcanzaron el mismo índice de confirmación.

Los resultados permiten analizar los mecanismos de replicación, consenso y recuperación de RabbitMQ, junto con la dependencia de la disponibilidad respecto de la mayoría de réplicas.
