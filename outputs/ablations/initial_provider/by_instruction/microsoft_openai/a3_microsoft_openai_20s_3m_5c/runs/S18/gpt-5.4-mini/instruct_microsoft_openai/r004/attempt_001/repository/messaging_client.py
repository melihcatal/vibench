import os

from azure.servicebus import ServiceBusClient


def get_connection_string():
    return os.environ["AZURE_SERVICEBUS_CONNECTION_STRING"]


def get_topic_name():
    return os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME", "pubsub-events")


def get_queue_name():
    return os.environ.get("AZURE_SERVICEBUS_QUEUE_NAME", "pubsub-events")


def get_dead_letter_queue_name():
    return os.environ.get("AZURE_SERVICEBUS_DEAD_LETTER_QUEUE_NAME", "pubsub-dead-letter")


def create_client():
    return ServiceBusClient.from_connection_string(get_connection_string())
