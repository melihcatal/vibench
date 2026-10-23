import os
import json
from confluent_kafka import Producer

# Load Confluent Kafka configuration from environment
bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
api_key = os.getenv('CONFLUENT_API_KEY')
if not bootstrap_servers or not api_key:
    raise RuntimeError('Set CONFLUENT_BOOTSTRAP_SERVERS and CONFLUENT_API_KEY environment variables')

# Configure Kafka producer
conf = {
    'bootstrap.servers': bootstrap_servers,
    'api.key': api_key,
    'client.id': 'publish_event_client'
}
producer = Producer(conf)

def publish_event(topic, event):
    """Publish a JSON event to a Kafka topic.
    Args:
        topic (str): The topic name.
        event (dict): JSON-serializable event payload.
    """
    try:
        producer.produce(topic=topic, value=json.dumps(event).encode('utf-8'))
        producer.flush()
        print(f'Successfully published event to {topic}')
    except Exception as e:
        print(f'Failed to publish event: {e}')

if __name__ == '__main__':
    sample_event = {
        'id': 'evt_001',
        'payload': {'message': 'Hello Pub/Sub'}
    }
    publish_event('my_topic', sample_event)
