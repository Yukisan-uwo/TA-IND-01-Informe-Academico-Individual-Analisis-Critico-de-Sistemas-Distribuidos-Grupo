# TA-IND-01 — Informe Académico Individual: Análisis Crítico de Sistemas Distribuidos

**Estudiante:** Herrera Barco Humberto Aldair  
**Asignatura:** Aplicaciones Distribuidas  
**Actividad:** TA-IND-01 — Análisis crítico comparativo de Elasticsearch y Apache Solr como sistemas distribuidos

## Descripción

Este directorio contiene el desarrollo del informe académico individual centrado en **Elasticsearch** como sistema distribuido principal y su comparación con **Apache Solr (SolrCloud)**. El análisis aplica conceptos de la Unidad 1 (transparencias de distribución, teorema CAP y extensión PACELC, modelos de comunicación y tolerancia a fallos), apoyado en revisión bibliográfica, documentación oficial y una experimentación propia sobre un clúster local.

## Sistemas analizados

- **Principal:** Elasticsearch
- **Comparación:** Apache Solr (SolrCloud)

## Estructura del directorio

- `main.tex`: documento principal del informe en LaTeX.
- `referencias.bib`: referencias bibliográficas (artículos y documentación oficial/fuentes técnicas) en formato BibLaTeX.
- `figuras/`: imágenes utilizadas en el informe.
  - `anexo_a_esquema_mano.jpeg`: esquema inicial a mano de la arquitectura.
  - `anexo_b_deniz_2023.png`, `anexo_b_calderon_2023.png`, `anexo_b_unger_2023.png`: capturas/anotaciones de lectura de fuentes (Anexo B).
  - `captura_01_cluster.png`: levantamiento y estado del clúster.
  - `captura_02_shards.png`: distribución de shards primarios y réplicas.
  - `captura_03_caida_nodo.png`: estado tras la caída de un nodo.
  - `captura_04_recuperacion.png`: recuperación y redistribución de shards.
  - `arquitectura_elasticsearch.png` _(pendiente)_: diagrama final de arquitectura exportado desde draw.io (ver nota).
- `capturas/`: capturas originales del experimento.
- `experimento/`: archivos del experimento.
  - `docker-compose.yml`: definición del clúster local de Elasticsearch (3 nodos).
  - `resultados.md`: comandos ejecutados, salidas e interpretaciones.
  - `indice.json`, `doc.json`: artefactos de apoyo del experimento.
- `BITACORA.md`: registro cronológico del trabajo realizado.

## Experimentación realizada

Se desplegó un clúster local de **Elasticsearch 8.15.0** con tres nodos (`es01`, `es02`, `es03`) mediante Docker Compose. Las pruebas incluyeron:

1. Levantamiento del clúster y verificación del estado (`green`, 3 nodos).
2. Creación del índice `pruebas` con 3 shards primarios y 1 réplica, inserción de 6 documentos y verificación de la distribución de shards.
3. Simulación de fallo deteniendo `es02` y observación del comportamiento del clúster (mantenimiento de shards activos/estado).
4. Recuperación al reiniciar `es02` y verificación de la redistribución de shards.

Los detalles y evidencias se documentan en `experimento/resultados.md` y en las capturas de `figuras/`.

## Compilación del informe (LaTeX)

El documento usa `pdflatex` + `biber` + `biblatex` (estilo IEEE).

### Overleaf

1. Subir `main.tex`, `referencias.bib` y la carpeta `figuras/` al proyecto (manteniendo las rutas relativas).
2. En **Menu**: `Compiler = pdfLaTeX`, `TeX Live version = 2024/2025` (o reciente), `Main document = main.tex`.
3. Presionar **Recompile** (Overleaf ejecuta automáticamente la secuencia necesaria para bibliografía).
4. Descargar el PDF desde el visor.

### Compilación local

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

## Notas

- Se incluyen las **6 referencias de artículos** requeridas, además de algunas referencias de **documentación oficial** utilizadas para sustentar aspectos técnicos del análisis.
