import os
import json
from confluent_kafka import Producer

# Load Confluent Kafka config from env vars
bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
api_key = os.getenv('CONFLUENT_API_KEY')
if not bootstrap_servers or not api_key:
    raise RuntimeError('Set CONFLUENT_BOOTSTRAP_SERVERS and CONFLUENT_API_KEY')

conf = {
    'bootstrap.servers': bootstrap_servers,
    'api.key': api_key,
    'client.id': 'batch_publisher'
}
producer = Producer(conf)

def publish_batch(topic, messages):
    """Publish a list of JSON messages to a Kafka topic in a single batch.",
    topic (str): Topic name.",
    messages (list[dict]): List of JSON-serializable messages.",
    """
    try:
        for msg in messages:
            producer.produce(topic, value=json.dumps(msg).encode('utf-8'))
        producer.flush()
        print(f'Batch of {len(messages)} messages sent to {topic}')
    except Exception as e:
        print(f'Batch publish failed: {e}')

if __name__ == '__main__':
    batch = [
        {'id': 'msg_1', 'payload': {'text': 'Hello'}},
        {'id': 'msg_2', 'payload': {'text': 'World'}},
    ]
    publish_batch('my_topic', batch)
