#!/usr/bin/env python3
# Produtor 1: Sensor de Temperatura
# Publica leituras brutas na fila raw_temperatures

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rabbitpy
import json
import time
import random
from datetime import datetime
from config import *

def main():
    # Conectar ao RabbitMQ
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'

    with rabbitpy.Connection(url) as conn:
        with conn.channel() as channel:
            # Criar fila
            queue = rabbitpy.Queue(channel, QUEUE_RAW_TEMPERATURES)
            queue.declare()

            print("=" * 60)
            print("SENSOR DE TEMPERATURA - PRODUTOR 1")
            print("=" * 60)
            print(f"RabbitMQ: {RABBITMQ_HOST}")
            print(f"Fila: {QUEUE_RAW_TEMPERATURES}")
            print(f"Sensor: {SENSOR_ID}")
            print(f"Faixa: {TEMP_MIN}°C - {TEMP_MAX}°C")
            print(f"Intervalo: {READING_INTERVAL_SECONDS}s")
            print("=" * 60)

            current_temp = random.uniform(TEMP_MIN, TEMP_MAX)
            iteration = 0

            try:
                while True:
                    iteration += 1

                    # Variação gradual
                    variation = random.uniform(-0.5, 0.5)
                    current_temp += variation
                    current_temp = max(TEMP_MIN, min(TEMP_MAX, current_temp))

                    # Criar mensagem
                    message = {
                        "sensor_id": SENSOR_ID,
                        "temperature": round(current_temp, 2),
                        "timestamp": datetime.now().isoformat()
                    }

                    # Publicar
                    msg = rabbitpy.Message(channel, json.dumps(message))
                    msg.publish('', QUEUE_RAW_TEMPERATURES)

                    print(f"[{iteration:04d}] {message['timestamp'][:19]} | 🌡️  {message['temperature']:5.2f}°C")

                    time.sleep(READING_INTERVAL_SECONDS)

            except KeyboardInterrupt:
                print(f"\n\nProdutor interrompido. Total: {iteration} leituras")

if __name__ == "__main__":
    main()
