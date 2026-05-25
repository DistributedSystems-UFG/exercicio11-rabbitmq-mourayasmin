#!/usr/bin/env python3
# Testa o pipeline completo publicando 5 mensagens

import rabbitpy
import json
import time
from config import *

url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'

print("=" * 70)
print("TESTE DE PIPELINE: Publicando 5 temperaturas na fila")
print("=" * 70)

with rabbitpy.Connection(url) as conn:
    with conn.channel() as channel:
        queue = rabbitpy.Queue(channel, QUEUE_RAW_TEMPERATURES)
        queue.declare()

        for i in range(1, 6):
            message = {
                "sensor_id": SENSOR_ID,
                "temperature": 20.0 + i,
                "timestamp": f"2024-01-01T00:0{i}:00"
            }

            msg = rabbitpy.Message(channel, json.dumps(message))
            msg.publish('', QUEUE_RAW_TEMPERATURES)

            print(f"✓ Mensagem {i} publicada: {message['temperature']}°C")
            time.sleep(0.5)

print("\n" + "=" * 70)
print("AGORA VERIFIQUE:")
print("=" * 70)
print("Terminal 1 (statistics_consumer): Deve mostrar cálculos")
print("Terminal 2 (storage_consumer): Deve mostrar 'Estatística armazenada'")
print()
print("Aguarde 5 segundos e execute:")
print("  python3 view_stats.py")
print("=" * 70)
