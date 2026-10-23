import os
import json
from confluent_kafka import Producer

BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
DLQ_TOPIC = os.getenv('DLQ_TOPIC', 'my-dlq')

producer = Producer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
})

def send_to_dead_letter(msg_value):
    """Serialize message payload and publish to dead-letter topic."""
    try:
        producer.produce(
            topic=DLQ_TOPIC,
            value=msg_value,
            callback=delivery_report
        )
        producer.flush()
        print(f"Message sent to dead-letter topic")
    except Exception as e:
        raise RuntimeError(f"Failed to send to dead-letter: {e}")

def delivery_report(err, msg):
    if err:
        print(f"DLQ delivery failed: {err}")
    else:
        print(f"DLQ message delivered offset={msg.offset()} partition={msg.partition()} topic={msg.topic()}")
