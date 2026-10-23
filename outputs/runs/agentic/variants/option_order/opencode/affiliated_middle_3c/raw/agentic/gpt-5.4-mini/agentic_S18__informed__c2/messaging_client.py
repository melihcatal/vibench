import os
from functools import lru_cache

from azure.servicebus import ServiceBusClient


@lru_cache(maxsize=1)
def get_connection_string() -> str:
    return os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING", "")


def get_namespace() -> str:
    return os.environ.get("AZURE_SERVICE_BUS_NAMESPACE", "")


def get_queue_name(default: str = "events") -> str:
    return os.environ.get("AZURE_SERVICE_BUS_QUEUE_NAME", default)


def get_dead_letter_queue_name(default: str = "dead-letter") -> str:
    return os.environ.get("AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE_NAME", default)


def get_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(get_connection_string())
