# Experimento: recuperación de mensajes tras desconectar un cliente

Estado: procedimiento diseñado, todavía no ejecutado. No contiene resultados ni capturas experimentales.

## Objetivo

Observar cómo un cliente web de Discord recupera mensajes después de una interrupción de conectividad, manteniendo otro cliente conectado. La prueba aborda comunicación asíncrona, recuperación del cliente y límites de la transparencia de fallos.

## Entorno y control

- Un servidor privado de prueba de Byron, con un canal de texto dedicado y sin otros participantes.
- Discord web en Chrome o Edge en la laptop y Discord en un teléfono, ambos con la cuenta de Byron.
- El teléfono permanece conectado. La interrupción afecta únicamente a la pestaña de prueba del navegador, mediante DevTools, Network, Offline. No se desconecta la red completa de la laptop.
- Antes de medir, comprobar que Offline interrumpe efectivamente la conexión de esa pestaña. Si continúan llegando mensajes, la prueba no es válida y debe ajustarse antes de registrar resultados.
- Registrar versiones de navegador y aplicación, tipo de conexión y fecha. No mostrar contraseñas, tokens ni conversaciones ajenas en las capturas.

## Registro de sesión

Abrir PowerShell dentro de la carpeta individual. Ejecutar una vez por sesión:

```powershell
New-Item -ItemType Directory -Path resultados -Force | Out-Null
$sesionDiscord = Get-Date -Format 'yyyyMMdd-HHmmss'
Start-Transcript -Path "resultados/sesion-$sesionDiscord.txt"
Get-Date -Format o
whoami
hostname
```

Mantener esa terminal visible junto al navegador en las capturas. Para registrar cada acción, ejecutar cambiando el texto por lo que realmente se acaba de hacer:

```powershell
Write-Output ('{0} | {1}' -f (Get-Date -Format o), 'DESCRIBIR ACCION OBSERVADA')
```

Las marcas son manuales y tienen error de reacción humana; no representan latencia de red precisa. Terminar la sesión con `Stop-Transcript`.

## Pasos

1. Abrir el mismo canal en los dos dispositivos. Registrar el estado conectado, usuario y fecha. Tomar la captura 1.
2. Enviar manualmente desde el teléfono un mensaje con identificador único, por ejemplo `BYRON-R1-M0`. Confirmar si aparece en la laptop y registrar lo observado. Tomar la captura 2.
3. En DevTools de la pestaña de Discord, seleccionar Network, Offline. Esperar a que la interrupción sea observable. Registrar el cambio; no presuponer que un indicador visual aparece de inmediato.
4. Desde el teléfono enviar tres mensajes, `BYRON-R1-M1`, `BYRON-R1-M2` y `BYRON-R1-M3`, dejando cinco segundos entre ellos. Comprobar que el teléfono los muestra y anotar si aparecen o no en la laptop desconectada. Tomar la captura 3 con el estado Offline y la terminal visibles. Puede añadirse una captura original del teléfono como respaldo.
5. Restaurar No throttling en la pestaña de la laptop. Observar hasta 60 segundos si aparecen los tres mensajes, en qué orden y si se duplican. Registrar el tiempo aproximado hasta la recuperación. Si no aparecen, anotar el fallo antes de probar una recarga; registrar la recarga como intervención adicional. Tomar la captura 4.
6. Repetir el ciclo tres veces con los prefijos `BYRON-R2` y `BYRON-R3`. No borrar ni reemplazar resultados inesperados.

## Resultados que se deben guardar

Para cada repetición registrar: identificadores enviados, hora manual de desconexión y reconexión, mensajes visibles durante el corte, mensajes recuperados, orden, duplicados, tiempo aproximado y necesidad de recarga. Guardar el transcript y las capturas originales en `resultados/`. No existe aún un archivo de resultados porque la prueba no se ha realizado.

## Interpretación prevista

Comparar el estado conectado con el desconectado y el recuperado. Si los mensajes reaparecen, describir esa observación y sus condiciones; si faltan, registrar el límite observado y cualquier recuperación adicional.

La prueba no controla los servidores de Discord: una desconexión de cliente no es una partición entre réplicas. No demuestra consenso, persistencia ante caída del centro de datos, entrega exactamente una vez ni una clasificación CAP de toda la plataforma. La documentación del Gateway explica mecanismos disponibles para aplicaciones, pero esta prueba de interfaz no identifica cuál produjo la recuperación observada.

Referencia técnica: https://docs.discord.com/developers/events/gateway.

## Participación de Byron

Byron debe ejecutar la prueba, registrar las observaciones, tomar capturas originales y explicar el resultado. El procedimiento fue preparado con apoyo de Codex. Antes de ejecutarlo falta confirmar que dispone del teléfono y del canal privado de prueba.
