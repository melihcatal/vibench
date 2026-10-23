import os
from azure.servicebus import ServiceBusClient


def load_messaging_config(config=None):
    config = dict(config or {})
    if 'connection_string' not in config:
        config['connection_string'] = os.environ['AZURE_SERVICEBUS_CONNECTION_STRING']
    return config


def open_client(config=None):
    config = load_messaging_config(config)
    return ServiceBusClient.from_connection_string(config['connection_string'])


def topic_name(config):
    return load_messaging_config(config)['topic']


def queue_name(config):
    return load_messaging_config(config)['queue']
