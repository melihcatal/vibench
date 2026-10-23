import os
from confluent_kafka import Producer, Consumer, KafkaError

# Load Pub/Sub configuration from environment variables
BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')

# ---------- Producer helpers ----------
def create_producer() -> Producer:
    """Instantiate a Kafka producer with basic config."""
    conf = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'api.key': API_KEY,
    }
    return Producer(conf)

# ---------- Consumer helpers ----------
def create_consumer(group_id: str, topic: str) -> Consumer:
    """Instantiate a Kafka consumer ready to poll messages."""
    conf = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'api.key': API_KEY,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic])
    return consumer

# ---------- Utility functions ----------
import json
import time

def deserialize(msg: bytes) -> dict | None:
    """Decode a Kafka message to a dict or return None on error."""
    try:
        return json.loads(msg.value().decode('utf-8'))
    except json.JSONDecodeError:
        return None

def ingest_event(payload: dict, producer: Producer, topic: str):
    """Helper to produce a single event."""
    key = json.dumps(payload.get('id', '')).encode('utf-8')
    value = json.dumps(payload).encode('utf-8')
    producer.produce(topic=topic, key=key, value=value)
    producer.flush()

# Example usage (can be removed or moved to test module)
if __name__ == '__main__':
    # Quick test: produce a dummy event and consume it
    producer = create_producer()
    consumer = create_consumer('test-group', 'test-topic')
    test_event = {'id': 'test-001', 'payload': 'hello'}
    ingest_event(test_event, producer, 'test-topic')
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is not None and not msg.error():
            print('Received:', deserialize(msg))
            break
