import os
import json
from confluent_kafka import Producer

BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
TOPIC = os.getenv('PUBSUB_TOPIC', 'my-events')

producer = Producer({
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
})

def publish_batch(events):
    """Publish a list of dict events to the same Kafka topic.
    Each event must have a unique 'id' field.
    """
    try:
        for ev in events:
            producer.produce(
                topic=TOPIC,
                key=str(ev['id']),
                value=json.dumps(ev),
                callback=delivery_report
            )
        producer.flush()
        print(f"Batch of {len(events)} events published")
    except Exception as e:
        raise RuntimeError(f"Error in batch publish: {e}")

def delivery_report(err, msg):
    if err is not None:
        print(f"Batch delivery failed for key {msg.key()}: {err}")
        # Optionally re-queue or route to DLQ
    else:
        print(f"Batch delivered to {msg.topic()} [{msg.partition()}] offset={msg.offset()}")
