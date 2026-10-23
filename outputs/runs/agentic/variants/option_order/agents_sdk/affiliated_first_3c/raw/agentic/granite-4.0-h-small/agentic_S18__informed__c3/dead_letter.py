import os
import json
from confluent_kafka import Producer, KafkaException

# Load configuration for primary and dead-letter topics
BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')
DLQ_TOPIC = os.getenv('DEAD_LETTER_TOPIC', 'my-dlq')
PRIMARY_TOPIC = os.getenv('PUBSUB_TOPIC', 'my-topic')

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
}

dlq_producer = Producer(conf)

def send_to_dead_letter(original_msg: dict, error_info: str):
    """Send a failed message to a dead-letter topic with additional error metadata.
    Args:
        original_msg: dict containing the original payload.
        error_info: string describing why processing failed.
    """
    dlq_payload = {
        'original': original_msg,
        'error': error_info,
        'timestamp': str(int(time.time()))
    }
    dlq_key = json.dumps(original_msg.get('id', '')).encode('utf-8')
    dlq_value = json.dumps(dlq_payload).encode('utf-8')
    dlq_producer.produce(topic=DLQ_TOPIC, key=dlq_key, value=dlq_value)
    dlq_producer.flush()
