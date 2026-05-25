#!/usr/bin/env python3
# Script para testar conexão com RabbitMQ

import rabbitpy
from config import *

def test_connection():
    """Testa conexão com RabbitMQ"""
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}'

    print("=" * 60)
    print("TESTE DE CONEXÃO RABBITMQ")
    print("=" * 60)
    print(f"Host: {RABBITMQ_HOST}:{RABBITMQ_PORT}")
    print(f"Vhost: {RABBITMQ_VHOST}")
    print(f"Usuário: {RABBITMQ_USER}")
    print("=" * 60)

    try:
        with rabbitpy.Connection(url) as conn:
            print("✓ Conexão estabelecida com sucesso!")

            with conn.channel() as channel:
                print("✓ Canal criado com sucesso!")

                # Testar criação das filas
                for queue_name in [QUEUE_RAW_TEMPERATURES, QUEUE_PROCESSED_STATS, QUEUE_ALERTS]:
                    queue = rabbitpy.Queue(channel, queue_name)
                    queue.declare()
                    print(f"✓ Fila '{queue_name}' criada/verificada")

        print("\n" + "=" * 60)
        print("SUCESSO! Sistema pronto para uso.")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        print("\nVerifique:")
        print("1. RabbitMQ está rodando?")
        print("2. Credenciais corretas em config.py?")
        print("3. Firewall permite acesso à porta 5672?")

if __name__ == "__main__":
    test_connection()
