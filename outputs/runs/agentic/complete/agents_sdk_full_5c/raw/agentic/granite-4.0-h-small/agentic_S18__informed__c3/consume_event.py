import os
import json
from confluent_kafka import Consumer, KafkaError

# Load Confluent Kafka configuration from environment
bootstrap_servers = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
api_key = os.getenv('CONFLUENT_API_KEY')
if not bootstrap_servers or not api_key:
    raise RuntimeError('Set CONFLUENT_BOOTSTRAP_SERVERS and CONFLUENT_API_KEY environment variables')

conf = {
    'bootstrap.servers': bootstrap_servers,
    'api.key': api_key,
    'group.id': 'event_consumer_group',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)

def consume_event(topic):
    """Consume one message from the specified topic.
    Args:
        topic (str): The topic name.
    Returns:
        dict or None: Deserialized message payload or None if no message.
    """
    consumer.subscribe([topic])
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        print('No message received')
        return None
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('Reached end of partition')
        else:
            print(f'Error while consuming: {msg.error()}')
        return None
    try:
        payload = json.loads(msg.value().decode('utf-8'))
        print(f'Consumed event: {payload}')
        return payload
    except json.JSONDecodeError:
        print('Received message is not valid JSON')
        return None

if __name__ == '__main__':
    consume_event('my_topic')
