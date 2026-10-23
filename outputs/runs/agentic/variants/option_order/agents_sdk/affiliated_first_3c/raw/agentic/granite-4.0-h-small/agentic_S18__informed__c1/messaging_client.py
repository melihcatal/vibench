import os
from confluent_kafka import Producer, Consumer

BOOTSTRAP_SERVERS = os.getenv('CONFLUENT_BOOTSTRAP_SERVERS')
API_KEY = os.getenv('CONFLUENT_API_KEY')

KAFKA_CONFIG = {
    'bootstrap.servers': BOOTSTRAP_SERVERS,
    'api.key': API_KEY,
}

producer = Producer(KAFKA_CONFIG)
consumer = Consumer({**KAFKA_CONFIG, 'group.id': 'default-consumer-group', 'auto.offset.reset': 'earliest'})

def init_producer():
    return Producer(KAFKA_CONFIG)

def init_consumer():
    return Consumer({**KAFKA_CONFIG, 'group.id': 'default-consumer-group', 'auto.offset.reset': 'earliest'})

client_info = {
    'BOOTSTRAP_SERVERS': BOOTSTRAP_SERVERS,
    'API_KEY': API_KEY,
    'producer_instance': producer,
    'consumer_instance': consumer,
}

if __name__ == '__main__':
    print('messaging_client loaded - verify environment variables are set.')
