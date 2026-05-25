# Configurações compartilhadas

# RabbitMQ
from const import RABBITMQ_ADDR

RABBITMQ_HOST = RABBITMQ_ADDR
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'myuser'
RABBITMQ_PASSWORD = 'abc123'
RABBITMQ_VHOST = 'my_vhost'

# Filas
QUEUE_RAW_TEMPERATURES = 'raw_temperatures'
QUEUE_PROCESSED_STATS = 'processed_stats'
QUEUE_ALERTS = 'temperature_alerts'

# Sensor
SENSOR_ID = 'sensor-001'
TEMP_MIN = 20.0
TEMP_MAX = 35.0
TEMP_NORMAL_MIN = 22.0
TEMP_NORMAL_MAX = 28.0
READING_INTERVAL_SECONDS = 3

# Database
DATABASE_PATH = 'temperature.db'

# Processamento
WINDOW_SIZE = 10  # Número de leituras para calcular estatísticas
