# Prueba de disponibilidad de lectura en Apache Cassandra

**Fecha de ejecución:** 12 de noviembre de 2026  
**Entorno:** Windows PowerShell 5.1 y Docker Desktop  
**Versión probada:** Apache Cassandra 5.0.9  
**Clúster:** `TAIND01`, con tres nodos en el centro de datos `dc1`

## 1. Objetivo

Comprobar si Cassandra puede devolver el mismo registro con los niveles de
consistencia `ONE` y `QUORUM` cuando quedan tres, dos o una réplica activa.
Durante la prueba mantuve encendido `taind-cas1` y usé ese nodo para coordinar
todas las consultas.

[Esquema inicial dibujado a mano](../esquema-inicial.jpeg)

## 2. Preparación del clúster en Docker

Ejecuté estos comandos en PowerShell:

```powershell
docker version
docker pull cassandra:5.0
docker network create taind-cassandra
```

- `docker version` comprueba que la terminal puede comunicarse con el motor de Docker.
- `docker pull cassandra:5.0` descarga la imagen de la serie 5.0. La versión exacta que usé fue 5.0.9.
- `docker network create taind-cassandra` crea la red interna por la que se comunican los tres contenedores.

### 2.1. Primer nodo

```powershell
docker run -d --name taind-cas1 --hostname taind-cas1 --network taind-cassandra -e CASSANDRA_CLUSTER_NAME=TAIND01 -e CASSANDRA_DC=dc1 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e MAX_HEAP_SIZE=768M -e HEAP_NEWSIZE=192M cassandra:5.0

docker exec taind-cas1 nodetool status
```

`docker run -d` crea el contenedor y lo deja ejecutándose en segundo plano.
`--name` le da el nombre que uso desde PowerShell, `--hostname` fija su nombre
interno y `--network` lo conecta a la red del laboratorio.

Las opciones `-e` establecen variables de entorno. En este caso definen el
nombre del clúster (`TAIND01`), el centro de datos (`dc1`), el mecanismo que
identifica la ubicación de los nodos por centro de datos y rack, y los tamaños
de memoria de la máquina virtual de Java.

`docker exec` ejecuta un comando dentro de un contenedor que ya está activo.
`nodetool status` muestra los nodos que Cassandra reconoce. Una fila `UN`
indica que el nodo está activo y en estado normal (*Up/Normal*).

La primera consulta devolvió este mensaje durante el arranque:

```text
Error: No nodes present in the cluster. Has this node finished starting up?
```

Revisé las últimas 60 líneas del registro y volví a consultar el estado:

```powershell
docker logs --tail 60 taind-cas1
docker exec taind-cas1 nodetool status
```

El registro mostró `Startup complete`. Al repetir `nodetool status`, apareció
una fila `UN` en `dc1` con la dirección `172.18.0.2`.

### 2.2. Segundo y tercer nodo

Primero arranqué el nodo 2:

```powershell
docker run -d --name taind-cas2 --hostname taind-cas2 --network taind-cassandra -e CASSANDRA_SEEDS=taind-cas1 -e CASSANDRA_CLUSTER_NAME=TAIND01 -e CASSANDRA_DC=dc1 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e MAX_HEAP_SIZE=768M -e HEAP_NEWSIZE=192M cassandra:5.0

docker exec taind-cas1 nodetool status
```

`CASSANDRA_SEEDS=taind-cas1` le indica al nodo nuevo con qué nodo puede
contactar para descubrir el clúster. La primera consulta de estado todavía
mostraba una sola fila. Al repetirla, aparecieron dos filas `UN`.

Cuando los dos primeros nodos estuvieron activos, inicié el tercero:

```powershell
docker run -d --name taind-cas3 --hostname taind-cas3 --network taind-cassandra -e CASSANDRA_SEEDS=taind-cas1 -e CASSANDRA_CLUSTER_NAME=TAIND01 -e CASSANDRA_DC=dc1 -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e MAX_HEAP_SIZE=768M -e HEAP_NEWSIZE=192M cassandra:5.0

Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec taind-cas1 nodetool version
docker exec taind-cas1 nodetool status
```

`Get-Date` muestra la fecha y hora en la terminal. `nodetool version` confirmó
la versión 5.0.9 y `nodetool status` mostró tres filas `UN` en `dc1`.

[Captura 1. Clúster con tres nodos activos](../Evidencias/01-cluster-tres-nodos.jpeg)

## 3. Creación del registro de prueba

Abrí `cqlsh` desde PowerShell:

```powershell
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec -it taind-cas1 cqlsh
```

`-it` abre una sesión interactiva. `cqlsh` es el cliente de Cassandra que
permite ejecutar instrucciones en CQL. Al abrirlo dentro de `taind-cas1`,
se conectó al puerto `9042` de ese contenedor. Por eso el nodo 1 recibió y
coordinó las consultas.

Con los tres nodos activos, ejecuté estas instrucciones en `cqlsh`:

```sql
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

- `CREATE KEYSPACE` crea el espacio `laboratorio`. `NetworkTopologyStrategy`
  permite configurar la replicación por centro de datos. El valor `3` asigna
  tres réplicas a los datos de este espacio en `dc1`.
- `CREATE TABLE` crea la tabla `eventos`. `id` es la clave primaria y
  `descripcion` guarda el texto del registro.
- `IF NOT EXISTS` permite ejecutar la instrucción de creación aunque el
  objeto ya exista.
- `CONSISTENCY ALL` fija el nivel de consistencia de la sesión hasta que se
  cambie. El `INSERT` debe recibir la confirmación de las tres réplicas.
- `INSERT` guarda el registro con `id = 1`. La terminal volvió a `cqlsh>`
  sin mostrar un error.

## 4. Procedimiento y resultados

En cada escenario repetí estas instrucciones en `cqlsh`:

```sql
CONSISTENCY ONE;
SELECT * FROM laboratorio.eventos WHERE id = 1;

CONSISTENCY QUORUM;
SELECT * FROM laboratorio.eventos WHERE id = 1;
```

`SELECT` recupera el mismo registro en cada escenario. `ONE` exige la
respuesta de una réplica. `QUORUM` exige una mayoría de las réplicas
configuradas, que en esta prueba corresponde a dos de tres.

### 4.1. Lectura con tres réplicas activas

Con los tres nodos activos, ambas consultas devolvieron una fila:

```text
 id | descripcion
----+-----------------------
  1 | Prueba de replicacion

(1 rows)
```

[Captura 2. Lecturas con tres réplicas activas](../Evidencias/02-lecturas-tres-replicas.png)

### 4.2. Lectura con dos réplicas activas

En una ventana de PowerShell, detuve el nodo 3 y consulté el estado del
clúster desde el nodo 1:

```powershell
docker stop taind-cas3
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec taind-cas1 nodetool status
```

`docker stop` detiene el contenedor indicado. `nodetool status` permite
comprobar que el clúster lo ve como caído (`DN`). Después repetí las lecturas
con `ONE` y `QUORUM` desde `cqlsh`.

**Resultado observado:** [Completar con lo que devolvió cada consulta en la captura 3.]

[Captura 3. Lecturas con dos réplicas activas](../Evidencias/03-lecturas-dos-replicas.png)

### 4.3. Lectura con una réplica activa

Con el nodo 3 todavía detenido, detuve también el nodo 2:

```powershell
docker stop taind-cas2
Get-Date -Format "yyyy-MM-dd HH:mm:ss"
docker exec taind-cas1 nodetool status
```

Volví a abrir `cqlsh` en `taind-cas1` y repetí las mismas lecturas. `ONE`
devolvió el registro `id = 1` con la descripción `Prueba de replicacion`.
La consulta con `QUORUM` devolvió esta salida:

```text
NoHostAvailable: ('Unable to complete the operation against any hosts', {<Host: 127.0.0.1:9042 dc1>: Unavailable('Error from server: code=1000 [Unavailable exception] message="Cannot achieve consistency level QUORUM" info={\'consistency\': \'QUORUM\', \'required_replicas\': 2, \'alive_replicas\': 1}')})
```

Dentro del mensaje, `required_replicas: 2` indica cuántas réplicas exigía la
lectura y `alive_replicas: 1` indica cuántas estaban disponibles.

[Captura 4. Lecturas con una réplica activa](../Evidencias/04-lecturas-una-replica.png)

## 5. Interpretación

Al detener dos nodos, pude seguir leyendo el registro con `ONE` porque
bastaba la respuesta de la única réplica activa. Al repetir la misma consulta
con `QUORUM`, Cassandra devolvió `Unavailable` porque necesitaba dos réplicas
disponibles. El nivel de consistencia elegido determinó si podía completar
la lectura durante la detención controlada de los nodos.

## 6. Restablecimiento del clúster

Para volver a encender los contenedores detenidos y verificar su estado:

```powershell
docker start taind-cas2 taind-cas3
docker exec taind-cas1 nodetool status
```

`docker start` vuelve a encender los contenedores que ya existen. El clúster
está listo cuando `nodetool status` vuelve a mostrar tres filas `UN` en `dc1`.
