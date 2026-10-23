import os
from azure.servicebus import ServiceBusClient


def load_messaging_config(config=None):
    config = config or {}
    return {
        'connection_string': config.get('connection_string') or os.environ.get('AZURE_SERVICE_BUS_CONNECTION_STRING'),
        'topic': config.get('topic') or os.environ.get('AZURE_SERVICE_BUS_TOPIC'),
        'subscription': config.get('subscription') or os.environ.get('AZURE_SERVICE_BUS_SUBSCRIPTION'),
        'queue': config.get('queue') or os.environ.get('AZURE_SERVICE_BUS_QUEUE'),
        'dead_letter_queue': config.get('dead_letter_queue') or os.environ.get('AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE'),
    }


def build_service_bus_client(config=None):
    config = load_messaging_config(config)
    return ServiceBusClient.from_connection_string(config['connection_string'])
