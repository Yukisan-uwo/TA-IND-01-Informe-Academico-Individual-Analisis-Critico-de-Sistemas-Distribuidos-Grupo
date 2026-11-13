
import os
import socket
from datetime import datetime

import pika

COLA = "taind01_mensajes"
MAX_MENSAJES = 5

credenciales = pika.PlainCredentials(
    "laboratorio",
    os.environ["RABBITMQ_PASSWORD"]
)

parametros = pika.ConnectionParameters(
    host="127.0.0.1",
    port=5672,
    credentials=credenciales,
    blocked_connection_timeout=30
)

conexion = pika.BlockingConnection(parametros)

try:
    canal = conexion.channel()

    # Comprobar que la cola existe
    canal.queue_declare(queue=COLA, passive=True)

    print("=== PRUEBA 5: CONSUMIDOR RABBITMQ ===")
    print("Equipo:", socket.gethostname())
    print("Fecha:", datetime.now().astimezone().isoformat())
    print("Cola:", COLA)

    recibidos = 0

    for _ in range(MAX_MENSAJES):
        metodo, propiedades, cuerpo = canal.basic_get(
            queue=COLA,
            auto_ack=False
        )

        if metodo is None:
            print("No quedan mensajes disponibles.")
            break

        try:
            mensaje = cuerpo.decode("utf-8")

            print(f"\nMensaje recibido: {mensaje}")
            print("ID:", propiedades.message_id)
            print("Reentregado:", metodo.redelivered)

            # Confirmar despues de procesar el mensaje
            canal.basic_ack(
                delivery_tag=metodo.delivery_tag
            )

            recibidos += 1
            print("ACK manual enviado correctamente.")

        except Exception:
            canal.basic_nack(
                delivery_tag=metodo.delivery_tag,
                requeue=True
            )
            raise

    print("\nTotal de mensajes procesados:", recibidos)

finally:
    if conexion.is_open:
        conexion.close()
