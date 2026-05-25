#!/usr/bin/env python3
# Consumidor 1: Processador de Estatísticas
# Consome de raw_temperatures, calcula estatísticas e publica em processed_stats

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rabbitpy
import json
from collections import deque
from datetime import datetime
from config import *

class StatisticsProcessor:
    def __init__(self):
        self.readings = deque(maxlen=WINDOW_SIZE)

    def add_reading(self, temp):
        self.readings.append(temp)

    def calculate_stats(self):
        if not self.readings:
            return None

        temps = list(self.readings)
        return {
            'avg_temperature': round(sum(temps) / len(temps), 2),
            'min_temperature': round(min(temps), 2),
            'max_temperature': round(max(temps), 2),
            'sample_count': len(temps),
            'timestamp': datetime.now().isoformat()
        }

def main():
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'
    processor = StatisticsProcessor()

    with rabbitpy.Connection(url) as conn:
        with conn.channel() as channel:
            # Criar filas
            queue_in = rabbitpy.Queue(channel, QUEUE_RAW_TEMPERATURES)
            queue_in.declare()

            queue_out = rabbitpy.Queue(channel, QUEUE_PROCESSED_STATS)
            queue_out.declare()

            print("=" * 70)
            print("PROCESSADOR DE ESTATÍSTICAS - CONSUMIDOR 1")
            print("=" * 70)
            print(f"Consumindo de: {QUEUE_RAW_TEMPERATURES}")
            print(f"Publicando em: {QUEUE_PROCESSED_STATS}")
            print(f"Janela de cálculo: {WINDOW_SIZE} leituras")
            print("=" * 70)

            msg_count = 0

            try:
                for message in queue_in:
                    data = json.loads(message.body.decode())
                    msg_count += 1

                    # Adicionar leitura
                    processor.add_reading(data['temperature'])

                    # Calcular estatísticas
                    stats = processor.calculate_stats()

                    if stats:
                        stats['sensor_id'] = data['sensor_id']

                        # Publicar
                        stats_msg = rabbitpy.Message(channel, json.dumps(stats))
                        stats_msg.publish('', QUEUE_PROCESSED_STATS)

                        print(f"[{msg_count:04d}] Média: {stats['avg_temperature']:5.2f}°C | "
                              f"Min: {stats['min_temperature']:5.2f}°C | "
                              f"Max: {stats['max_temperature']:5.2f}°C | "
                              f"Amostras: {stats['sample_count']}")

                    message.ack()

            except KeyboardInterrupt:
                print(f"\n\nProcessador interrompido. Total: {msg_count} mensagens")

if __name__ == "__main__":
    main()
