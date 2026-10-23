import os
from typing import Optional

from azure.servicebus import ServiceBusClient


def get_connection_string() -> str:
    value = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING", "")
    if not value:
        raise RuntimeError("AZURE_SERVICE_BUS_CONNECTION_STRING is required")
    return value


def get_topic_name(default: str = "events") -> str:
    return os.getenv("AZURE_SERVICE_BUS_TOPIC_NAME", default)


def get_queue_name(default: str = "events") -> str:
    return os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", default)


def create_client(connection_string: Optional[str] = None) -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(
        connection_string or get_connection_string()
    )
