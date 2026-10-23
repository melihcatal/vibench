import os
from azure.servicebus import ServiceBusClient


def get_client(config=None):
    config = config or {}
    connection_string = config.get('connection_string', os.getenv('AZURE_SERVICEBUS_CONNECTION_STRING'))
    topic = config.get('topic', os.getenv('AZURE_SERVICEBUS_TOPIC'))
    queue = config.get('queue', os.getenv('AZURE_SERVICEBUS_QUEUE'))
    dead_letter_queue = config.get('dead_letter_queue', os.getenv('AZURE_SERVICEBUS_DEAD_LETTER_QUEUE'))
    return ServiceBusClient.from_connection_string(connection_string), topic, queue, dead_letter_queue