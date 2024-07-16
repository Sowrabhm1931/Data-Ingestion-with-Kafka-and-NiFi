from confluent_kafka import Producer
import json

# Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092'
}

# Create Producer instance
p = Producer(**conf)

# Optional delivery report callback to confirm message delivery
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Produce messages to topic
topic = 'real-time-data'

# Create a sample message
message = {'key': 'value'}

# Produce the message
p.produce(topic, key='key', value=json.dumps(message), callback=delivery_report)

# Wait up to 1 second for events. Callbacks will be invoked during
# the call to poll() if the message is acknowledged or fails.
p.poll(1)

# Wait for any outstanding messages to be delivered and delivery reports
# to be received.
p.flush()

