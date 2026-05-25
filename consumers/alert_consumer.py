#!/usr/bin/env python3
# Consumidor 3: Monitor de Alertas
# Consome e exibe alertas de temperatura

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rabbitpy
import json
from config import *

def main():
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'

    with rabbitpy.Connection(url) as conn:
        with conn.channel() as channel:
            # Criar fila
            queue = rabbitpy.Queue(channel, QUEUE_ALERTS)
            queue.declare()

            print("=" * 60)
            print("MONITOR DE ALERTAS - CONSUMIDOR 3")
            print("=" * 60)
            print(f"Consumindo de: {QUEUE_ALERTS}")
            print(f"Faixa normal: {TEMP_NORMAL_MIN}°C - {TEMP_NORMAL_MAX}°C")
            print("=" * 60)

            alert_count = 0

            try:
                for message in queue:
                    data = json.loads(message.body.decode())
                    alert_count += 1

                    symbol = "🔵" if data['alert_type'] == "BAIXA" else "🔴"

                    print(f"{symbol} ALERTA #{data['alert_id']}: "
                          f"Temperatura {data['alert_type']} detectada!")
                    print(f"   Sensor: {data['sensor_id']}")
                    print(f"   Temperatura: {data['temperature']:.2f}°C")
                    print(f"   Horário: {data['timestamp'][:19]}")
                    print("-" * 60)

                    message.ack()

            except KeyboardInterrupt:
                print(f"\n\nMonitor interrompido. Total: {alert_count} alertas processados")

if __name__ == "__main__":
    main()
