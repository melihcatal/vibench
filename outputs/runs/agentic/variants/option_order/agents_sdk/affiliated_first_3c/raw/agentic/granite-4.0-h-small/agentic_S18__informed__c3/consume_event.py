import os
import json
from confluent_kafka import Consumer, KafkaException

# Load configuration from environment variables
BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'my-consumer-group')
TOPIC = os.getenv('PUBSUB_TOPIC', 'my-topic')

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(conf)
consumer.subscribe([TOPIC])

def consume_event() -> dict | None:
    """Poll a single message and deserialize its JSON payload.
    Returns:
        dict of the message payload or None if poll times out.
    """
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        return None
    if msg.error():
        # Requeue on permanent error, otherwise ignore transient errors.
        raise KafkaException(msg.error())
    # msg.value() holds the decoded payload previously sent by publish_event.
    return json.loads(msg.value().decode('utf-8'))

if __name__ == '__main__':
    # Example loop: consume one message and print it.
    while True:
        event = consume_event()
        if event:
            print('Consumed event:', event)
            # After processing, commit offset (handled automatically when using higher-level libraries)
        else:
            print('No message received, try again.')
