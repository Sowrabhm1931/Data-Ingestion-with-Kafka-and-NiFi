from confluent_kafka import Consumer, KafkaException, KafkaError

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

# Create Consumer instance
c = Consumer(**conf)

# Subscribe to topic
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
    # Close down consumer to commit final offsets.
    c.close()

