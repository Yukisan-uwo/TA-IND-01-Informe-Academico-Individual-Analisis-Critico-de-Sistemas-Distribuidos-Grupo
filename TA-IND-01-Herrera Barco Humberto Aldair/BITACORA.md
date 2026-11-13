# Bitácora

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
