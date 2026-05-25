#!/usr/bin/env python3
# Script para visualizar estatísticas do banco de dados

import sqlite3
from config import DATABASE_PATH

def view_statistics():
    """Exibe estatísticas armazenadas no banco"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Contar total de registros
        cursor.execute("SELECT COUNT(*) FROM statistics")
        total = cursor.fetchone()[0]

        print("=" * 80)
        print(f"ESTATÍSTICAS ARMAZENADAS (Total: {total} registros)")
        print("=" * 80)

        # Buscar últimos 20 registros
        cursor.execute("""
            SELECT id, sensor_id, avg_temperature, min_temperature, max_temperature,
                   sample_count, timestamp
            FROM statistics
            ORDER BY id DESC
            LIMIT 20
        """)

        print(f"\n{'ID':<5} {'Sensor':<12} {'Média':<8} {'Min':<8} {'Max':<8} "
              f"{'Amostras':<10} {'Timestamp'}")
        print("-" * 80)

        for row in cursor.fetchall():
            id, sensor_id, avg_temp, min_temp, max_temp, sample_count, timestamp = row
            print(f"{id:<5} {sensor_id:<12} {avg_temp:>6.2f}°C {min_temp:>6.2f}°C "
                  f"{max_temp:>6.2f}°C {sample_count:<10} {timestamp[:19]}")

        # Estatísticas gerais
        cursor.execute("""
            SELECT
                MIN(min_temperature) as overall_min,
                MAX(max_temperature) as overall_max,
                AVG(avg_temperature) as overall_avg
            FROM statistics
        """)

        overall_min, overall_max, overall_avg = cursor.fetchone()

        if overall_min and overall_max and overall_avg:
            print("\n" + "=" * 80)
            print("ESTATÍSTICAS GERAIS")
            print("=" * 80)
            print(f"Temperatura Mínima Absoluta: {overall_min:.2f}°C")
            print(f"Temperatura Máxima Absoluta: {overall_max:.2f}°C")
            print(f"Temperatura Média Geral: {overall_avg:.2f}°C")
            print("=" * 80)

        conn.close()

    except sqlite3.OperationalError:
        print("⚠️  Banco de dados ainda não criado ou tabela não existe.")
        print("Execute os componentes para gerar dados primeiro.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    view_statistics()
