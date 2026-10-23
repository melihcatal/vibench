import os
from azure.servicebus import ServiceBusClient


def load_messaging_config(config=None):
    config = config or {}
    return {
        'connection_string': config.get('connection_string') or os.environ['AZURE_SERVICEBUS_CONNECTION_STRING'],
        'topic': config.get('topic') or os.environ.get('AZURE_SERVICEBUS_TOPIC', 'events'),
        'subscription': config.get('subscription') or os.environ.get('AZURE_SERVICEBUS_SUBSCRIPTION', 'events-subscription'),
        'queue': config.get('queue') or os.environ.get('AZURE_SERVICEBUS_QUEUE', 'events-queue'),
        'dead_letter_queue': config.get('dead_letter_queue') or os.environ.get('AZURE_SERVICEBUS_DEAD_LETTER_QUEUE', 'events-dead-letter'),
        'audit_table': config.get('audit_table') or os.environ.get('AZURE_STORAGE_TABLE_NAME', 'messageaudit'),
        'translator_resource': config.get('translator_resource') or os.environ.get('AZURE_TRANSLATOR_TEXT_ENDPOINT'),
        'translator_key': config.get('translator_key') or os.environ.get('AZURE_TRANSLATOR_TEXT_KEY'),
        'safety_endpoint': config.get('safety_endpoint') or os.environ.get('AZURE_CONTENT_SAFETY_ENDPOINT'),
        'safety_key': config.get('safety_key') or os.environ.get('AZURE_CONTENT_SAFETY_KEY'),
    }


def get_servicebus_client(config=None):
    cfg = load_messaging_config(config)
    return ServiceBusClient.from_connection_string(cfg['connection_string']), cfg
