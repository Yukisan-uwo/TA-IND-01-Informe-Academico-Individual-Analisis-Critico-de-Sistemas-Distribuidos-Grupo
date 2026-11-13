
import os
import socket
from datetime import datetime

import pika

COLA = "taind01_mensajes"

# Conexion al primer nodo del cluster
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

    # Verificar que la cola ya existe
    canal.queue_declare(queue=COLA, passive=True)

    # Solicitar confirmaciones del broker
    canal.confirm_delivery()

    print("=== PRUEBA 5: PRODUCTOR RABBITMQ ===")
    print("Equipo:", socket.gethostname())
    print("Fecha:", datetime.now().astimezone().isoformat())
    print("Cola:", COLA)

    for numero in range(1, 6):
        mensaje = (
            f"TA-IND-01 | Python mensaje {numero:03d} "
            f"| equipo={socket.gethostname()}"
        )

        canal.basic_publish(
            exchange="",
            routing_key=COLA,
            body=mensaje.encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
                content_type="text/plain",
                message_id=f"TAIND01-{numero:03d}"
            ),
            mandatory=True
        )

        print(f"Confirmado por RabbitMQ: {mensaje}")

    print("Publicaciones confirmadas: 5")

finally:
    if conexion.is_open:
        conexion.close()
