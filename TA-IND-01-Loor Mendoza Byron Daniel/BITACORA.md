# Bitácora de trabajo

## 2026-11-11 - Organización inicial

- Byron dedicó aproximadamente 1 h a ordenar los planteamientos y preparar el trabajo. Ese día creó su carpeta en el repositorio.

## 2026-11-12 - Preparación inicial con apoyo de Codex

- Actividad: revisión de la consigna TA-IND-01, clonación del repositorio compartido e identificación de la carpeta individual. Preparación del README con el alcance y los entregables pendientes.
- Problema encontrado: el primer acceso remoto mediante Git falló en el entorno restringido.
- Resolución: se repitió la clonación con acceso autorizado y se verificó el contenido del repositorio.
- Avance posterior de la sesión: Byron eligió Discord. Se revisaron las referencias del repositorio GHLZ, se identificaron fuentes reutilizables y se consultaron documentación oficial de Discord, la especificación de Matrix y páginas editoriales de dos artículos. Se delimitó el análisis a mensajes de texto y se propuso Matrix como comparación.
- Estado: no se ha ejecutado el experimento ni completado la verificación bibliográfica. La confirmación del tema registrado y de las formativas sigue pendiente.
- Byron recuerda haber trabajado desde la tarde y continuado hasta cerca de las 02:00 del viernes. La hora de inicio del jueves y las pausas no quedaron registradas.
- Revisión del estudiante: pendiente. Esta entrada describe acciones realizadas con apoyo de Codex.

### Preparación del aporte del día

- Se contrastaron los metadatos de tres artículos con sus fichas editoriales y se prepararon seis entradas en referencias.bib, incluidas tres fuentes técnicas.
- Se revisaron las correcciones del artículo de Ferreira: retirada de una cifra y cambio de la figura 4. Se documentaron los límites de la verificación y las lecturas personales pendientes en REVISION-FUENTES.md.
- No se encontró el comando Docker en la terminal. Se preparó una prueba de desconexión de Discord web con un segundo dispositivo conectado, sin instalar herramientas.
- EXPERIMENTO.md contiene los pasos, comandos de registro, cuatro capturas previstas, tres repeticiones y límites de interpretación. La ejecución está pendiente de Byron.
- Los cambios fueron preparados con apoyo de Codex. No se han generado evidencias personales ni resultados experimentales.
- Byron redactó los tres mensajes de commit para tema, fuentes y procedimiento. Se organizaron los archivos en esos tres avances para su publicación.

### Preparación del entorno y de la comparación con Zulip

- Byron eligió Zulip para la comparación. Se actualizó la bibliografía con su arquitectura, el flujo de envío de mensajes y la configuración de PostgreSQL en un servidor separado.
- Se incorporó el informe técnico de Discord sobre la caída de autenticación del 6 de noviembre de 2023 como caso para estudiar tolerancia a fallos.
- Con apoyo de Codex se instaló MiKTeX 25.12. Se comprobó que pdfLaTeX y Biber 2.21 generan una página de prueba con citas IEEE y las nueve entradas bibliográficas.
- Se precisaron los pasos para registrar el corte y la reconexión en Discord web. La ejecución con el celular se registró en la sesión siguiente.

### Piloto en la PC

- Byron creó el servidor privado de prueba y abrió el canal en Chrome. Codex operó Chrome y el navegador integrado durante la ronda piloto.
- Chrome recibió el mensaje de control y también recibió el segundo mensaje mientras DevTools indicaba `Offline`. Se restauró `No throttling` y se registró el resultado en EXPERIMENTO.md.
- El control no aisló a Chrome. Para la prueba principal se usará el celular con datos móviles y un corte real de conexión en la laptop.
- A petición de Byron, Codex redactó los mensajes de los dos commits de esta actualización tomando como referencia los tres mensajes anteriores que él escribió.

### Borrador del informe

- Con apoyo de Codex se preparó main.tex con la estructura de la consigna, las referencias IEEE y el resultado del piloto asistido. Se anotaron las secciones por completar y los comandos para compilar.
- Las capturas originales y las observaciones de la prueba con el celular se incorporaron en la sesión siguiente.

## 2026-11-13 - Primera ronda del experimento

- Byron ejecutó la prueba de desconexión y reconexión con Chrome y el celular. Al recuperar la conexión, los tres mensajes aparecieron sin recargar Chrome.
- La hora exacta de reconexión quedó sin medir. Se conservó la hora original de la captura y se registró la confirmación de Byron en el informe y en EXPERIMENTO.md.
- Se ordenaron las fuentes del informe, el procedimiento y las capturas. Se verificó que los archivos originales de las capturas conservaran el mismo contenido al moverlos. Se incorporó el ejemplo de Byron sobre el aviso «Reconectando».
- Byron cerró la transcripción de PowerShell. Se comprobó que conserva el registro del mensaje de control, las anotaciones del corte y la observación posterior a la reconexión.
- Byron envió ZULIP-M1 en el tema Prueba TA-IND-01 del canal general de la demo. Codex preparó el borrador del mensaje, comprobó que el mensaje siguiera visible al volver al tema y guardó la captura para el informe.
- Codex ubicó los fragmentos de tres artículos citados para el Anexo B. Tras intentar marcarlos en Brave, Byron guardó el resaltado en los PDF de Ferreira (p. 14), Bação y Guerreiro (p. 4) y Kokociński (p. 11). Codex tomó en Edge las capturas con las marcas y el número de página visibles.
- Codex redactó los mensajes de los commits de la prueba de Discord, el borrador comparativo y la incorporación de las lecturas. Los mensajes de autoría del estudiante se registran en sus propios commits.
- Byron compartió la foto del bosquejo que dibujó el 12 de noviembre. Codex incorporó el archivo original al Anexo A y añadió la referencia al bosquejo en la sección de arquitectura.
- Se actualizó la declaración de uso de IA para precisar el apoyo de Codex y las comprobaciones que Byron realizó en el experimento y al marcar los artículos. Queda pendiente el cotejo personal de los DOI.
- Codex preparó el diagrama editable a partir del bosquejo de Byron y ayudó a exportarlo e incorporarlo en la sección de arquitectura. Byron confirmó la facultad, el nivel, el paralelo y la fecha de la carátula.
- Se cotejó el borrador con el encuadre de Aplicaciones Distribuidas. Se fijó el diagrama en la sección de arquitectura y se regeneró el PDF desde una copia limpia de los archivos del informe.
- Byron contrastó con Codex las dos referencias de Springer. Codex comprobó los datos de Kokociński y colaboradores en la ficha de Elsevier y el PDF. Se precisó la conclusión sobre lo observado en Chrome y los límites de la prueba. Codex redactó el mensaje del commit de este avance.
- La sesión del jueves continuó durante la madrugada del viernes hasta cerca de las 02:00, según recuerda Byron. Dentro de esa sesión, la transcripción estuvo abierta desde las 23:39 del jueves hasta las 00:43 del viernes. Esa ventana de 1 h 4 min ya está incluida en la sesión.
- Byron retomó el trabajo aproximadamente a las 11:00 y continuó hasta las 13:00. Dedicó unas 2 h a la sesión del mediodía, en la que revisó la arquitectura, confirmó la carátula y cotejó las referencias.
- Codex registró las duraciones comunicadas por Byron y redactó el mensaje del commit de la bitácora.
