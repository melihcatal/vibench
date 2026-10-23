import os
import json
from confluent_kafka import Producer

# Load configuration from environment variables
BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
TOPIC = os.getenv('PUBSUB_TOPIC', 'my-topic')

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
}

producer = Producer(conf)

def publish_event(payload: dict):
    """Publish a JSON event as a Kafka message.
    Args:
        payload: dict representing the event.
    """
    key = json.dumps(payload.get('id', '')).encode('utf-8')
    value = json.dumps(payload).encode('utf-8')
    producer.produce(topic=TOPIC, key=key, value=value)
    producer.flush()

if __name__ == '__main__':
    # Example usage: publish a sample event
    sample_event = {"id": "msg-001", "content": "Hello Pub/Sub"}
    publish_event(sample_event)
