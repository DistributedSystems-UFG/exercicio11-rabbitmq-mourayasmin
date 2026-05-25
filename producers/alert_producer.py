#!/usr/bin/env python3
# Produtor 2: Gerador de Alertas
# Consome da fila raw_temperatures e publica alertas quando temperatura anormal

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rabbitpy
import json
from datetime import datetime
from config import *

def main():
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'

    with rabbitpy.Connection(url) as conn:
        with conn.channel() as channel:
            # Criar filas
            queue_in = rabbitpy.Queue(channel, QUEUE_RAW_TEMPERATURES)
            queue_in.declare()

            queue_out = rabbitpy.Queue(channel, QUEUE_ALERTS)
            queue_out.declare()

            print("=" * 60)
            print("GERADOR DE ALERTAS - PRODUTOR 2")
            print("=" * 60)
            print(f"Consumindo de: {QUEUE_RAW_TEMPERATURES}")
            print(f"Publicando em: {QUEUE_ALERTS}")
            print(f"Faixa normal: {TEMP_NORMAL_MIN}°C - {TEMP_NORMAL_MAX}°C")
            print("=" * 60)

            alert_count = 0

            try:
                for message in queue_in:
                    data = json.loads(message.body.decode())
                    temp = data['temperature']

                    # Verificar se está fora do normal
                    if temp < TEMP_NORMAL_MIN or temp > TEMP_NORMAL_MAX:
                        alert_count += 1

                        alert_type = "BAIXA" if temp < TEMP_NORMAL_MIN else "ALTA"

                        alert = {
                            "alert_id": alert_count,
                            "sensor_id": data['sensor_id'],
                            "temperature": temp,
                            "alert_type": alert_type,
                            "timestamp": datetime.now().isoformat(),
                            "original_timestamp": data['timestamp']
                        }

                        # Publicar alerta
                        alert_msg = rabbitpy.Message(channel, json.dumps(alert))
                        alert_msg.publish('', QUEUE_ALERTS)

                        print(f"⚠️  ALERTA {alert_count}: Temperatura {alert_type} ({temp:.2f}°C)")

                    message.ack()

            except KeyboardInterrupt:
                print(f"\n\nProdutor de alertas interrompido. Total: {alert_count} alertas")

if __name__ == "__main__":
    main()
