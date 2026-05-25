#!/usr/bin/env python3
# Consumidor 2: Persistência
# Consome de processed_stats e armazena no SQLite

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import rabbitpy
import json
import sqlite3
from config import *

def init_database():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id TEXT,
            avg_temperature REAL,
            min_temperature REAL,
            max_temperature REAL,
            sample_count INTEGER,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()

def main():
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'

    # Inicializar banco
    init_database()
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    with rabbitpy.Connection(url) as rmq_conn:
        with rmq_conn.channel() as channel:
            # Criar fila
            queue = rabbitpy.Queue(channel, QUEUE_PROCESSED_STATS)
            queue.declare()

            print("=" * 60)
            print("ARMAZENAMENTO - CONSUMIDOR 2")
            print("=" * 60)
            print(f"Consumindo de: {QUEUE_PROCESSED_STATS}")
            print(f"Banco de dados: {DATABASE_PATH}")
            print("=" * 60)

            stored_count = 0

            try:
                for message in queue:
                    data = json.loads(message.body.decode())
                    stored_count += 1

                    # Inserir no banco
                    cursor.execute('''
                        INSERT INTO statistics
                        (sensor_id, avg_temperature, min_temperature, max_temperature, sample_count, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        data['sensor_id'],
                        data['avg_temperature'],
                        data['min_temperature'],
                        data['max_temperature'],
                        data['sample_count'],
                        data['timestamp']
                    ))

                    conn.commit()

                    print(f"✓ [{stored_count:04d}] Estatística armazenada | "
                          f"Média: {data['avg_temperature']:.2f}°C")

                    message.ack()

            except KeyboardInterrupt:
                print(f"\n\nArmazenamento interrompido. Total: {stored_count} registros")
            finally:
                conn.close()

if __name__ == "__main__":
    main()
