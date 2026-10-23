import json
import os

# Load Confluent Kafka client configuration from env vars
bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
api_key = os.getenv('CONFLUENT_API_KEY')
if not bootstrap_servers or not api_key:
    raise RuntimeError('Set CONFLUENT_BOOTSTRAP_SERVERS and CONFLUENT_API_KEY')

conf = {
    'bootstrap.servers': bootstrap_servers,
    'api.key': api_key,
    'client.id': 'messaging_client'
}

def get_producer():
    """Create and return a Kafka producer instance.",
    """
    from confluent_kafka import Producer
    return Producer(conf)

def get_consumer(group_id='default_consumer'):
    """Create and return a Kafka consumer instance.",
    group_id (str): Consumer group identifier.",
    """
    from confluent_kafka import Consumer
    return Consumer({**conf, 'group.id': group_id})

# Optional shared helpers
# Normalize payload to dict
parse_json = lambda value: json.loads(value.decode('utf-8')) if isinstance(value, bytes) else value
