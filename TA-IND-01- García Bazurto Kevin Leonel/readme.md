
# TA-IND-01 — Análisis crítico de Apache Cassandra

**Estudiante:** Kevin Leonel García Bazurto  
**Asignatura:** Aplicaciones Distribuidas  
**Paralelo:** A  
**Universidad:** Universidad Técnica Estatal de Quevedo

## ¿Qué investigué?

Probé si Apache Cassandra podía devolver el mismo registro al reducir de
tres a una las réplicas activas. Monté un clúster de tres nodos en Docker
y repetí una consulta CQL con los niveles de consistencia `ONE` y `QUORUM`.

| Réplicas activas | Lectura con `ONE` | Lectura con `QUORUM` |
| --- | --- | --- |
| 3 | Devolvió el registro | Devolvió el registro |
| 2 | Devolvió el registro | Devolvió el registro |
| 1 | Devolvió el registro | Falló por falta de réplicas disponibles |

Con una sola réplica activa, Cassandra devolvió el dato con `ONE`.
Con `QUORUM`, informó que necesitaba dos réplicas y que solo había una
disponible. La prueba se hizo sobre un registro escrito antes de detener
los nodos.

## Video de sustentación

En el video muestro la captura de una réplica activa y explico por qué
la misma consulta obtuvo dos resultados distintos al cambiar el nivel
de consistencia.

[Ver video de sustentación en YouTube](https://youtu.be/83_cYspvM3c)

## Archivos del trabajo

- [Informe en LaTeX](./INFORME%20TA-IND-01.tex)
- [Referencias bibliográficas](./referencias.bib)
- [Experimento con comandos, resultados e interpretación](./Experimento/prueba-cassandra.md)
- [Capturas de la práctica y de lectura de fuentes](./Evidencias/)
- [Diagrama editable de la arquitectura en Docker](./Evidencias/diagrama%20de%20arquitectura%20de%20Cassandra%20en%20Docker.drawio)
- [Esquema inicial dibujado a mano](./esquema-inicial.jpeg)
- [Bitácora de trabajo](./BITACORA.md)
