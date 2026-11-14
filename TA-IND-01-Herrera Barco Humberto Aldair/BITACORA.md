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
- Organicé las evidencias gráficas: renombré las imágenes de anexos en `figuras/` (`anexo_a_esquema_mano.jpeg`, `anexo_b_deniz_2023.png`, `anexo_b_calderon_2023.png`, `anexo_b_unger_2023.png`) y copié/renombré las capturas del experimento desde `capturas/` a `figuras/` (`captura_01_cluster.png`, `captura_02_shards.png`, `captura_03_caida_nodo.png`, `captura_04_recuperacion.png`) para integrarlas en el informe.
- Actualicé `referencias.bib` incorporando referencias de documentación oficial de Elasticsearch y Apache Solr, además de fuentes de incidentes/issues (`elastic_cloud_incident_2019`, `solr_jira_7844`), y las cité en `main.tex`.
- Completé y ajusté `main.tex`: incorporé las figuras del experimento y anexos, desarrollé el análisis/comparación con base en la Unidad 1 y la experimentación, y dejé pendientes solo los datos personales/evidencias propias que debo completar manualmente (paralelo, fecha, repositorio, ejemplos, declaración de IA y diagrama final exportado).
- Elaboré una propuesta de diagrama de arquitectura en draw.io (XML) coherente con el clúster de 3 nodos y la investigación, como guía para exportar `arquitectura_elasticsearch.png` y conservar el `.drawio`.
