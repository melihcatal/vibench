import os
import json
from confluent_kafka import Producer, KafkaException

# Load configuration from environment variables
BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
TOPIC = os.getenv('PUBSUB_TOPIC', 'my-batch-topic')

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
}

producer = Producer(conf)

def batch_publish(events: list[dict], partition: int = None):
    """Publish a list of events as Kafka messages in a single batch.
    Args:
        events: List of dicts, each representing an event.
        partition: Optional integer partition to publish all messages to.
    """
    for event in events:
        key = json.dumps(event.get('id', '')).encode('utf-8')
        value = json.dumps(event).encode('utf-8')
        try:
            producer.produce(topic=TOPIC, key=key, value=value, partition=partition)
        except KafkaException as e:
            # For demo, simply raise; production could retry or DLQ handling
            raise e
    producer.flush()

if __name__ == '__main__':
    sample_batch = [
        {'id': 'msg-001', 'content': 'Batch msg A'},
        {'id': 'msg-002', 'content': 'Batch msg B'},
        {'id': 'msg-003', 'content': 'Batch msg C'},
    ]
    batch_publish(sample_batch)
