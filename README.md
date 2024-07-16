# Kafka NiFi Project

This project demonstrates the integration of Apache Kafka, Apache NiFi, and a Python producer/consumer using `confluent_kafka`.

## Prerequisites

- Apache Kafka
- Apache Zookeeper
- Apache NiFi
- Python 3.x

## Setup

### Step 1: Install Kafka and Zookeeper

1. Download and extract Kafka.
2. Start Zookeeper:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    ```
3. Start Kafka:
    ```bash
    bin/kafka-server-start.sh config/server.properties
    ```

### Step 2: Set Up NiFi

1. Download and extract NiFi.
2. Start NiFi:
    ```bash
    bin/nifi.sh start
    ```
3. Create a NiFi flow with `GenerateFlowFile` and `PublishKafka_2_6` processors.
4. Configure `PublishKafka_2_6` with the following properties:
    - Kafka Brokers: `localhost:9092`
    - Topic Name: `real-time-data`

### Step 3: Create Python Producer and Consumer

1. Create and activate a virtual environment:
    ```bash
    python3 -m venv kafka-env
    source kafka-env/bin/activate
    ```
2. Install `confluent_kafka`:
    ```bash
    pip install confluent_kafka
    ```
3. Create `producer.py` and `consumer.py` with the following contents:

#### `producer.py`
```python
from confluent_kafka import Producer
import json

conf = {
    'bootstrap.servers': 'localhost:9092'
}

p = Producer(**conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

topic = 'real-time-data'
message = {'key': 'value'}

p.produce(topic, key='key', value=json.dumps(message), callback=delivery_report)
p.poll(1)
p.flush()

#### `consumer.py`
```python
from confluent_kafka import Consumer, KafkaException, KafkaError

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

c = Consumer(**conf)
topic = 'real-time-data'
c.subscribe([topic])

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        print(f'Received message: {msg.value().decode("utf-8")}')
except KeyboardInterrupt:
    pass
finally:
    c.close()

### Step 4: Run the Scripts

1. Run the producer:
    ```bash
    python producer.py
    ```

2. Run the consumer:
    ```bash
    python consumer.py
    ```
