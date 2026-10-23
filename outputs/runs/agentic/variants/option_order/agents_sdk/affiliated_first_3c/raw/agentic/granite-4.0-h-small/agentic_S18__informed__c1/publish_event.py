import os
import json
from confluent_kafka import Producer

# Load configuration from environment variables
BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
TOPIC = os.getenv('PUBSUB_TOPIC', 'my-events')

producer = Producer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
})

def publish_event(event: dict):
    try:
        producer.produce(
            topic=TOPIC,
            key=str(event['id']),
            value=json.dumps(event),
            callback=delivery_report
        )
        producer.flush()
        print(f"Published event id {event['id']}")
    except Exception as e:
        raise RuntimeError(f"Error publishing event: {e}")

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
        # Route failed messages to dead-letter topic
        producer.produce(
            topic='my-dlq',
            key=msg.key(),
            value=msg.value(),
            callback=delivery_report
        )
        producer.flush()
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] {msg.offset()}")
