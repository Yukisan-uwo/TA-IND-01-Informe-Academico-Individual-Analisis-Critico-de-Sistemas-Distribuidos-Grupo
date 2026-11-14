# Bitácora de trabajo — TA-IND-01

**Estudiante:** Kevin Leonel García Bazurto  
**Sistema analizado:** Apache Cassandra

## 12 de noviembre de 2026 — Montaje del clúster y prueba de lectura

**Tiempo dedicado:** aproximadamente 2 horas de trabajo efectivo, repartidas en varias sesiones a lo largo del día.

### Actividades realizadas

Dibujé a mano el esquema inicial del clúster y subí la fotografía al repositorio. Luego levanté tres nodos de Cassandra 5.0.9 en Docker y verifiqué con `nodetool status` que los tres estaban activos (`UN`).

Creé la tabla `laboratorio.eventos` e inserté un registro con el nivel de consistencia `ALL`. Desde el nodo 1, repetí la misma consulta con `ONE` y `QUORUM` en tres escenarios, con tres, dos y una réplica activa.

### Problema y solución

Al consultar el estado del primer nodo durante el arranque, `nodetool` indicó que todavía no había nodos en el clúster. Revisé los registros con `docker logs --tail 60 taind-cas1` y encontré el mensaje `Startup complete`. Volví a ejecutar `nodetool status` y comprobé que el nodo ya aparecía como `UN`. Después continué con el segundo nodo.

### Resultado y evidencias

Con una sola réplica activa, `ONE` devolvió el registro. La lectura con `QUORUM` falló porque Cassandra necesitaba dos réplicas y solo tenía una disponible.

Organicé las cuatro capturas en [Evidencias](./Evidencias/) y documenté los comandos y resultados en [prueba-cassandra.md](./Experimento/prueba-cassandra.md).
## 13 de noviembre de 2026 — Diagrama, lectura y sustentación

**Tiempo dedicado:** 3 horas dedicadas incluso en la elaboración final del informe.

Pasé mi bosquejo a Draw.io para mostrar cómo estaban conectados los tres nodos de Cassandra en Docker. Revisé tres artículos, marqué los
fragmentos que usé en el informe y preparé las capturas para el Anexo B.

Al preparar la sustentación, volví a leer la salida de la prueba con una réplica activa. Me fijé en que el error de `QUORUM` indicaba dos
réplicas requeridas y una disponible. Usé esa captura para explicar en el video por qué `ONE` sí devolvió el registro.
