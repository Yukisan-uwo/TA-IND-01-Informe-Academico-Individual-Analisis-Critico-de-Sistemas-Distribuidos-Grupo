# Bitácora

## 11/11/2026

- Creé mi espacio de trabajo en el repositorio
- Investigué sobre sistemas distribuidos para tomar uno como principal y otro como comparación. Los candidatos fueron estos:
  - Principal: Apache Cassandra Comparación: MongoDB / DynamoDB (descartado: un compañero ya lo registró)
  - Principal: Apache Kafka Comparación: RabbitMQ (descartado: ya estaba tomado)
  - Principal: Redis Cluster Comparación: Hazelcast (descartado: Redis ya estaba tomado)
  - Principal: Hazelcast Comparación: Apache Ignite
  - **Elegido: Principal: Elasticsearch Comparación: Apache Solr**

## 12/11/2026

- Elegí **Elasticsearch** como sistema principal y **Apache Solr** para compararlo. Lo elegí porque tiene mucha documentación oficial y se puede levantar fácil con Docker.
- Hice el boceto a mano de la arquitectura: cliente, clúster con 3 nodos y los shards primarios (P) y réplicas (R) repartidos.
- Comprobé que tengo Docker y Docker Compose instalados y dejé listo el `docker-compose.yml` de 3 nodos.

## 13/11/2026

- Cloné el repositorio en el escritorio para trabajar desde ahí.
- **Problema 1:** `docker compose up` falló al principio porque Docker Desktop no estaba abierto. **Solución:** lo abrí y volví a ejecutarlo. Los 3 nodos subieron bien.
- Verifiqué el clúster: 3 nodos y estado `green`. **Captura 1:** `capturas/01_cluster_3_nodos.png`.
- **Problema 2:** `git mv` falló al corregir el nombre de la carpeta `experiemnto` (tenía un `.gitkeep` borrado). **Solución:** la renombré con `Rename-Item`, y el `git add` lo hice desde mi carpeta principal con la ruta bien escrita.
- Hice commit y push del compose y la captura 1.
- Creé un índice de prueba (`pruebas`) con 3 shards y 1 réplica, y le agregué 6 documentos. **Captura 2:** `capturas/02_distribucion_shards.png`.
- **Problema 3:** en la primera captura de shards la columna `docs` salía en 0. **Solución:** hice un `_refresh` del índice y volví a consultar; ya aparecieron los 6 documentos repartidos.
- Detuve el nodo `es02` con `docker stop` para probar la tolerancia a fallos. Los comandos de salud y shards se me cortaron al pegarlos, y como me demoré, cuando los ejecuté el clúster ya estaba en `green` con 2 nodos y el master había cambiado a `es03`. **Captura 3:** `capturas/03_caida_nodo.png`.
- Levanté `es02` otra vez y vi cómo volvió a unirse al clúster. **Captura 4:** `capturas/04_recuperacion.png`.
- Pasé los comandos y las salidas de las 4 capturas a `experimento/resultados.md` y empecé a escribir las interpretaciones.
