import json
import os
from confluent_kafka import Producer

# Load Env vars for dead-letter topic configuration
DL_TOPIC = os.getenv('DEAD_LETTER_TOPIC')
if not DL_TOPIC:
    raise RuntimeError('Set DEAD_LETTER_TOPIC environment variable')

# Reuse producer config from other modules (must be set in environment)
bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
api_key = os.getenv('CONFLUENT_API_KEY')
if not bootstrap_servers or not api_key:
    raise RuntimeError('Set CONFLUENT_BOOTSTRAP_SERVERS and CONFLUENT_API_KEY')

conf = {
    'bootstrap.servers': bootstrap_servers,
    'api.key': api_key,
    'client.id': 'dead_letter_producer'
}
producer = Producer(conf)

def send_to_dead_letter(original_topic, message):
    """Send a failed message to a dead-letter Kafka topic.",
    original_topic (str): The topic where publishing originally failed.",
    message (dict): The original message payload.",
    """
    dl_msg = {
        'original_topic': original_topic,
        'original_message': message,
        'reason': 'publish_failure',
        'timestamp': int(time.time())
    }
    try:
        producer.produce(DL_TOPIC, value=json.dumps(dl_msg).encode('utf-8'))
        producer.flush()
        print(f'Sent to dead-letter topic: {DL_TOPIC}')
    except Exception as e:
        print(f'Error sending to dead-letter topic: {e}')

if __name__ == '__main__':
    # Example usage
    send_to_dead_letter('my_topic', {'id': 'evt_999', 'payload': {'msg': 'error'}})
