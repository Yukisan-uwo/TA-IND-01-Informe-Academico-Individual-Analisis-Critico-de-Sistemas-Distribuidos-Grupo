# Prueba de disponibilidad de lectura en Apache Cassandra

**Estudiante:** Kevin Leonel García Bazurto  
**Fecha de ejecución:** 12 de noviembre de 2026  
**Entorno:** Windows PowerShell 5.1 y Docker Desktop  
**Versión utilizada:** Apache Cassandra 5.0.9  
**Clúster:** `TAIND01`, con tres nodos en el centro de datos `dc1`

## 1. Objetivo

Comprobar si Cassandra podía devolver el mismo registro con `ONE` y
`QUORUM` cuando quedaban tres, dos o una réplica activa. Mantuve encendido
`taind-cas1` para recibir y coordinar todas las consultas.

## 2. Preparación del clúster

Desde PowerShell preparé el entorno:

```powershell
docker version
docker pull cassandra:5.0
docker network create taind-cassandra
```

`docker version` permite comprobar que Docker responde. `docker pull`
descarga la imagen de la serie 5.0. `docker network create` crea la red
interna por la que se comunican los tres contenedores.

### 2.1. Primer nodo

```powershell
docker run -d --name taind-cas1 --hostname taind-cas1 --network taind-cassandra -e CASSANDRA_CLUSTER_NAME=TAIND01 -e CASSANDRA_DC=dc1 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e MAX_HEAP_SIZE=768M -e HEAP_NEWSIZE=192M cassandra:5.0

docker exec taind-cas1 nodetool status
```

`docker run -d` crea el contenedor y lo deja ejecutándose en segundo plano.
`--name` fija el nombre con el que se maneja desde PowerShell, `--hostname`
establece su nombre interno y `--network` lo conecta a la red del laboratorio.
Las opciones `-e` configuran el nombre del clúster, el centro de datos,
el mecanismo que identifica el centro de datos y el rack, y la memoria de Java.

La primera consulta de estado devolvió este mensaje durante el arranque:

```text
Error: No nodes present in the cluster. Has this node finished starting up?
```

Revisé el registro de arranque y volví a consultar el estado:

```powershell
docker logs --tail 60 taind-cas1
docker exec taind-cas1 nodetool status
```

`docker logs --tail 60` muestra las últimas 60 líneas del registro.
Después del arranque, `nodetool status` mostró una fila `UN` en `dc1`.
`UN` significa que el nodo está activo y en estado normal.

### 2.2. Segundo y tercer nodo

```powershell
docker run -d --name taind-cas2 --hostname taind-cas2 --network taind-cassandra -e CASSANDRA_SEEDS=taind-cas1 -e CASSANDRA_CLUSTER_NAME=TAIND01 -e CASSANDRA_DC=dc1 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e MAX_HEAP_SIZE=768M -e HEAP_NEWSIZE=192M cassandra:5.0

docker exec taind-cas1 nodetool status
```

`CASSANDRA_SEEDS=taind-cas1` indica al nodo nuevo con qué nodo puede
contactar para descubrir el clúster. La primera consulta aún mostraba
una sola fila. Al repetirla aparecieron dos filas `UN`.

Con los dos primeros nodos activos, inicié el tercero:

```powershell
docker run -d --name taind-cas3 --hostname taind-cas3 --network taind-cassandra -e CASSANDRA_SEEDS=taind-cas1 -e CASSANDRA_CLUSTER_NAME=TAIND01 -e CASSANDRA_DC=dc1 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e MAX_HEAP_SIZE=768M -e HEAP_NEWSIZE=192M cassandra:5.0

Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec taind-cas1 nodetool version
docker exec taind-cas1 nodetool status
```

`Get-Date` muestra la fecha y hora del equipo. `nodetool version` confirmó
Cassandra 5.0.9 y `nodetool status` mostró los tres nodos con estado `UN`.

[Captura 1. Estado inicial del clúster](../Evidencias/01-cluster-tres-nodos.jpeg)

## 3. Creación del registro de prueba

Abrí el cliente de Cassandra dentro del primer contenedor:

```powershell
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec -it taind-cas1 cqlsh
```

`docker exec -it` ejecuta `cqlsh` en una sesión interactiva dentro de
`taind-cas1`. El cliente se conectó a `127.0.0.1:9042` desde el contenedor.
El nodo 1 recibió las consultas y actuó como coordinador.

Con los tres nodos activos, ejecuté estas instrucciones en `cqlsh`:

```cql
CREATE KEYSPACE IF NOT EXISTS laboratorio
WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': 3};

CREATE TABLE IF NOT EXISTS laboratorio.eventos (
    id int PRIMARY KEY,
    descripcion text
);

CONSISTENCY ALL;

INSERT INTO laboratorio.eventos (id, descripcion)
VALUES (1, 'Prueba de replicacion');
```

- `CREATE KEYSPACE` crea el espacio `laboratorio` y configura tres
  réplicas en `dc1` con `NetworkTopologyStrategy`.
- `CREATE TABLE` crea la tabla `eventos`. `id` identifica el registro y
  `descripcion` almacena el texto.
- `IF NOT EXISTS` evita un error si el espacio o la tabla ya existen.
- `CONSISTENCY ALL` fija el nivel de consistencia de la sesión para que
  la escritura requiera la confirmación de las tres réplicas.
- `INSERT` guarda el registro con `id = 1`. La terminal volvió a
  `cqlsh>` sin mostrar un error.

## 4. Consultas y resultados

Repetí la misma consulta en los tres escenarios. Cambié el nivel de
consistencia entre una lectura y la siguiente:

```cql
CONSISTENCY ONE;
SELECT * FROM laboratorio.eventos WHERE id = 1;

CONSISTENCY QUORUM;
SELECT * FROM laboratorio.eventos WHERE id = 1;
```

`SELECT` consulta el mismo registro en cada prueba. `ONE` requiere la
respuesta de una réplica. Con un factor de replicación de tres,
`QUORUM` requiere dos respuestas.

### 4.1. Tres réplicas activas

Los tres nodos estaban activos. Las dos consultas devolvieron esta fila:

```text
 id | descripcion
----+-----------------------
  1 | Prueba de replicacion

(1 rows)
```

[Captura 2. Lecturas con tres réplicas activas](../Evidencias/02-lecturas-tres-replicas.png)

### 4.2. Dos réplicas activas

La captura de Docker Desktop muestra `taind-cas2` detenido y
`taind-cas1` y `taind-cas3` activos. Para reproducir ese estado
desde PowerShell, se puede usar:

```powershell
docker stop taind-cas2
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec taind-cas1 nodetool status
```

`docker stop` detiene el contenedor indicado. `nodetool status` permite
comprobar si el clúster ya detectó el nodo como caído (`DN`).

**Resultado observado:** con dos réplicas activas, `ONE` y `QUORUM`
devolvieron el registro `id = 1` con la descripción `Prueba de replicacion`.

[Captura 3. Lecturas con dos réplicas activas](../Evidencias/03-lecturas-dos-replicas.png)

### 4.3. Una réplica activa

En este escenario quedó activo `taind-cas1`. Para reproducirlo desde
el estado de la sección anterior, se puede detener `taind-cas3` y
comprobar el estado del clúster:

```powershell
docker stop taind-cas3
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec taind-cas1 nodetool status
```

Repetí ambas consultas desde `cqlsh` en el nodo 1. `ONE` devolvió el
registro `id = 1` con la descripción `Prueba de replicacion`. Al cambiar
a `QUORUM`, obtuve esta salida:

```text
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 dc1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level QUORUM" info={\'consistency\': \'QUORUM\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
```

`required_replicas: 2` indica cuántas réplicas exigía la lectura.
`alive_replicas: 1` indica cuántas estaban disponibles.

[Captura 4. Lecturas con una réplica activa](../Evidencias/04-lecturas-una-replica.png)

## 5. Interpretación

Con tres y con dos réplicas activas, los dos niveles permitieron leer
el registro. Cuando quedó una sola réplica, `ONE` siguió funcionando
y `QUORUM` devolvió `Unavailable`. En esta configuración, la misma
consulta tuvo distinta disponibilidad según el nivel seleccionado.

La prueba observó lecturas de un registro escrito antes de detener
los contenedores. Para evaluar qué versión se leería si el dato cambiara
durante el fallo, haría falta otra prueba con escrituras concurrentes.

## 6. Restablecimiento del clúster

Para volver al estado inicial:

```powershell
docker start taind-cas2 taind-cas3
docker exec taind-cas1 nodetool status
```

`docker start` enciende los contenedores existentes. Una vez que los nodos
terminen de arrancar, `nodetool status` debería volver a mostrar tres
filas `UN` en `dc1`.
