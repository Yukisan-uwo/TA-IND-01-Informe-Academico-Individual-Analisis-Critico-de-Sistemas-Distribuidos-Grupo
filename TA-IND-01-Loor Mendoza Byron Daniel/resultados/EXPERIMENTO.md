# Experimento: recuperación de mensajes tras desconectar un cliente

Se completó una ronda con dos dispositivos. Chrome mostró los tres mensajes al reconectar sin recarga manual. El piloto asistido se conserva como antecedente del método.

## Objetivo

Observar cómo un cliente web de Discord recupera mensajes después de una interrupción de conectividad, manteniendo otro cliente conectado. La prueba aborda comunicación asíncrona, recuperación del cliente y límites de la transparencia de fallos.

## Entorno y control

- Un servidor privado de prueba de Byron, con un canal de texto dedicado y sin otros participantes.
- Discord web en Chrome o Edge en la laptop y Discord en un teléfono, ambos con la cuenta de Byron.
- El teléfono usa datos móviles y permanece conectado durante toda la prueba. La laptop usa Wi-Fi, que se desconecta durante el corte. Verificar que la laptop no tenga otra conexión activa y que el teléfono siga enviando mensajes. Mostrar el indicador de red de Windows en la captura del corte.
- Registrar versiones de navegador y aplicación, tipo de conexión y fecha. No mostrar contraseñas, tokens ni conversaciones ajenas en las capturas.

## Prueba piloto en una sola PC

1. Abrir el mismo canal privado de prueba en Chrome y Edge, con la cuenta de Byron en ambos. Edge será el emisor y Chrome el receptor.
2. Con ambos conectados, enviar `BYRON-PILOTO-M0` desde Edge y comprobar que aparezca en Chrome. Capturar el estado inicial y la recepción en Chrome.
3. Activar `Network > Offline` en DevTools de Chrome. Mantener Edge conectado y enviar desde allí `BYRON-PILOTO-M1`. Registrar si el mensaje aparece en Chrome durante el corte y tomar la tercera captura. Si llega durante el corte, registrar que el aislamiento no funcionó.
4. Restaurar `No throttling` en Chrome. Registrar si aparece `BYRON-PILOTO-M1`, si hizo falta recargar y cuánto tardó aproximadamente. Tomar la cuarta captura.

En esta variante, los dos navegadores comparten la conexión física de la PC. Mantener activo el Wi-Fi durante toda la prueba. Guardar las cuatro capturas originales con el prefijo `piloto-` y aplicar el registro de PowerShell de la siguiente sección. Identificar como piloto las observaciones y la participación de Codex si las hubo.

### Resultado del piloto

El 12 de noviembre de 2026, en el canal privado `#general` de `TA-IND-01 Piloto`, se usó el navegador integrado como emisor y Chrome como receptor, ambos en la misma PC. Codex operó los dos clientes durante el piloto.

- A las 20:00, hora de Ecuador, se envió `BYRON-PILOTO-M0` y se verificó su recepción en Chrome.
- A las 20:02 se envió `BYRON-PILOTO-M1` con DevTools de Chrome en `Offline`. El mensaje apareció en Chrome mientras el selector todavía indicaba `Offline`.
- Se restauró `No throttling` y se comprobó que ambos mensajes seguían visibles.

El control de desconexión falló. Esta ronda muestra que el ajuste de DevTools no aisló al receptor en las condiciones observadas. Para medir recuperación, usar Chrome en la laptop y el celular con datos móviles. Verificar el corte de la laptop antes de enviar los mensajes de la ronda. La captura del piloto se vio durante la sesión de Codex. Queda pendiente guardar las cuatro capturas de la prueba principal.

## Registro de sesión

Abrir PowerShell y ejecutar una vez por sesión:

```powershell
Set-Location -LiteralPath 'D:\7mo Software\Aplicaciones Distribuidas\TA-IND-01\TA-IND-01-Loor Mendoza Byron Daniel'
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
3. Desconectar el Wi-Fi de la laptop. Verificar que el indicador de red muestre que está desconectada y registrar el momento del corte.
4. Desde el teléfono enviar tres mensajes, `BYRON-R1-M1`, `BYRON-R1-M2` y `BYRON-R1-M3`, dejando cinco segundos entre ellos. Comprobar que el teléfono los muestra y anotar cuáles aparecen en la laptop durante el corte. Tomar la captura 3 con el indicador de desconexión y la terminal visibles. Puede añadirse una captura original del teléfono como respaldo.
5. Reconectar el Wi-Fi de la laptop. Observar hasta 60 segundos si aparecen los tres mensajes, en qué orden y si se duplican. Registrar el tiempo aproximado hasta la recuperación. Si siguen faltando al terminar el plazo, registrar el resultado antes de probar una recarga. Tomar la captura 4.

## Resultados que se deben guardar

Registrar los identificadores enviados, el estado de conexión, los mensajes visibles y recuperados, su orden y si hizo falta recargar. Guardar la transcripción en `resultados/` y las imágenes originales en `resultados/capturas/`. Las horas anotadas a mano son marcas de observación.

### Primera ronda (R1)

La [transcripción original de PowerShell](sesion-20261112-233908.txt) contiene los comandos, sus salidas y la anotación que Byron escribió después de reconectar.

Byron ejecutó la prueba entre la noche del 12 y la madrugada del 13 de noviembre de 2026, hora de Ecuador. El [mensaje de control](capturas/02-mensaje-recibido.png) `BYRON-R1-M0` se veía en Chrome y su recepción quedó anotada en PowerShell a las 23:41 del día 12.

- [00:05 - Inicio del corte](capturas/03a-inicio-del-corte.png). Windows muestra el icono de red sin Internet y Chrome conserva el historial visible, incluido el mensaje de control.
- [00:09 - Chrome después del envío](capturas/03b-chrome-despues-del-envio.png). En el [celular](capturas/r1-envio-desde-celular.png) ya se veían `BYRON-R1-M1`, `BYRON-R1-M2` y `BYRON-R1-M3`. En esta captura de Chrome todavía no aparecen. PowerShell muestra un registro manual y la barra de tareas muestra el icono de Wi-Fi, por lo que esta imagen documenta lo que se veía en Chrome en ese momento.
- [00:19 - Estado después de reconectar](capturas/04-reconexion.png). Chrome muestra una entrada de cada uno de los tres mensajes en el orden M1, M2 y M3. Byron confirmó que aparecieron al reconectar, sin recargar Chrome. Las 00:19 son la hora de la captura. El instante de reconexión y el tiempo de recuperación quedaron sin medir.

## Interpretación

El cliente web conservó el historial visible durante el corte y mostró los tres mensajes después de recuperar la conexión. La recuperación fue automática en esta ronda desde la perspectiva de Byron. La aparición posterior de los mensajes ilustra la recuperación del estado visible de un cliente.

La prueba no controla los servidores de Discord: una desconexión de cliente no es una partición entre réplicas. No demuestra consenso, persistencia ante caída del centro de datos, entrega exactamente una vez ni una clasificación CAP de toda la plataforma. La documentación del Gateway explica mecanismos disponibles para aplicaciones, pero esta prueba de interfaz no identifica cuál produjo la recuperación observada.

[Discord Gateway](https://docs.discord.com/developers/events/gateway) · [Modo Offline en Chrome DevTools](https://developer.chrome.com/docs/devtools/network/reference/#offline)

## Participación de Byron

Byron ejecutó la primera ronda, tomó las capturas originales y confirmó cómo aparecieron los mensajes. Codex apoyó la preparación del procedimiento y la organización de los archivos.
