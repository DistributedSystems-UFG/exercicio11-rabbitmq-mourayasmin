[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/BK9AX0KL)

# Exercício 11 - RabbitMQ/AMQP
Sistema de Monitoramento de Temperatura com Múltiplas Filas

## Arquitetura

Sistema distribuído com **3 filas**, **2 produtores** e **3 consumidores** implementando a mesma regra de negócio do Exercício 09 (Kafka).

```
Sensor → raw_temperatures → Statistics Consumer → processed_stats → Storage → SQLite
            ↓
      Alert Producer → temperature_alerts → Alert Consumer
```

### Componentes

**Filas:**
- `raw_temperatures`: Leituras brutas de sensores (20-35°C)
- `processed_stats`: Estatísticas (média, min, max)
- `temperature_alerts`: Alertas de temperatura anormal

**Produtores:**
- `sensor_producer.py`: Simula sensor gerando temperaturas
- `alert_producer.py`: Gera alertas quando temperatura < 22°C ou > 28°C

**Consumidores:**
- `statistics_consumer.py`: Calcula estatísticas com janela de 10 leituras
- `storage_consumer.py`: Persiste estatísticas no SQLite
- `alert_consumer.py`: Exibe alertas formatados

## Setup RabbitMQ (já configurado na AWS)

### Portas (firewall/security group):
```
5671-5672
```

### Instalação no setup RabbitMQ (se necessário):
```bash
sudo ./install_rabbitmq.sh
sudo systemctl start rabbitmq-server
sudo rabbitmqctl add_user myuser abc123
sudo rabbitmqctl add_vhost my_vhost
sudo rabbitmqctl set_permissions -p my_vhost myuser ".*" ".*" ".*"
```

## Execução

### 1. Instalar dependências
```bash
pip3 install -r requirements.txt
```

### 2. Testar conexão
```bash
python3 test_connection.py
```

### 3. Executar componentes (5 terminais separados)

**Terminal 1: Consumidor de Estatísticas**
```bash
python3 consumers/statistics_consumer.py
```

**Terminal 2: Consumidor de Armazenamento**
```bash
python3 consumers/storage_consumer.py
```

**Terminal 3: Consumidor de Alertas**
```bash
python3 consumers/alert_consumer.py
```

**Terminal 4: Produtor Sensor**
```bash
python3 producers/sensor_producer.py
```

**Terminal 5: Produtor de Alertas**
```bash
python3 producers/alert_producer.py
```

### 4. Verificar dados armazenados

**Opção 1: Script de visualização (recomendado)**
```bash
python3 view_stats.py
```

**Opção 2: SQLite direto**
```bash
sqlite3 temperature.db "SELECT * FROM statistics ORDER BY id DESC LIMIT 10;"
```

## Estrutura de Arquivos

```
exercicio11-rabbitmq-mourayasmin/
├── config.py                      # Configurações compartilhadas
├── const.py                       # IP do servidor RabbitMQ
├── requirements.txt               # Dependências Python
├── test_connection.py             # Script de teste
├── producers/
│   ├── sensor_producer.py        # Produtor 1: Sensor
│   └── alert_producer.py         # Produtor 2: Alertas
├── consumers/
│   ├── statistics_consumer.py    # Consumidor 1: Estatísticas
│   ├── storage_consumer.py       # Consumidor 2: Armazenamento
│   └── alert_consumer.py         # Consumidor 3: Monitor
└── temperature.db                 # Banco SQLite (criado automaticamente)
```