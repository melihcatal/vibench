import os

from azure.servicebus import ServiceBusClient


def load_config(config=None):
    cfg = dict(config or {})
    if 'connection_string' not in cfg:
        cfg['connection_string'] = os.environ['SERVICEBUS_CONNECTION_STRING']
    if 'topic' not in cfg:
        cfg['topic'] = os.environ.get('SERVICEBUS_TOPIC', 'events')
    if 'queue' not in cfg:
        cfg['queue'] = os.environ.get('SERVICEBUS_QUEUE', 'events')
    if 'subscription' not in cfg:
        cfg['subscription'] = os.environ.get('SERVICEBUS_SUBSCRIPTION', 'events-sub')
    if 'dead_letter_queue' not in cfg:
        cfg['dead_letter_queue'] = os.environ.get('SERVICEBUS_DEAD_LETTER_QUEUE', 'dead-letter')
    return cfg


def get_client(config=None):
    cfg = load_config(config)
    return ServiceBusClient.from_connection_string(cfg['connection_string']), cfg
