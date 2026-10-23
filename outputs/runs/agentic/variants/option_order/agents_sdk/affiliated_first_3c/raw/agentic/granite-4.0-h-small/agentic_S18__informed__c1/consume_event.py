import os
import json
from confluent_kafka import Consumer, KafkaException

# Load configuration from environment variables
BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
TOPIC = os.getenv('PUBSUB_TOPIC', 'my-events')
GROUP_ID = os.getenv('CONSUMER_GROUP_ID', 'my-consumer-group')

consumer = Consumer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',
})

def consume_one():
    try:
        consumer.subscribe([TOPIC])
        msg = consumer.poll(timeout=5.0)
        if msg is None:
            print("No message received within timeout")
            return None
        if msg.error():
            raise KafkaException(msg.error())
        # Expect JSON payload
        payload = json.loads(msg.value().decode('utf-8'))
        print(f"Consumed message key={msg.key()} value={payload}")
        return payload
    except Exception as e:
        print(f"Error consuming message: {e}")
        raise
    finally:
        consumer.close()
