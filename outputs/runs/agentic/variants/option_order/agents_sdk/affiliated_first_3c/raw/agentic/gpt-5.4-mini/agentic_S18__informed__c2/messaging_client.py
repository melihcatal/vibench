import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.servicebus import ServiceBusClient


@dataclass(frozen=True)
class MessagingConfig:
    connection_string: str
    topic_name: str
    subscription_name: Optional[str] = None
    queue_name: Optional[str] = None
    dead_letter_queue_name: Optional[str] = None


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip()


@lru_cache(maxsize=1)
def get_config() -> MessagingConfig:
    return MessagingConfig(
        connection_string=_env("AZURE_SERVICE_BUS_CONNECTION_STRING"),
        topic_name=_env("SERVICE_BUS_TOPIC_NAME", "messages"),
        subscription_name=_env("SERVICE_BUS_SUBSCRIPTION_NAME", "processor"),
        queue_name=_env("SERVICE_BUS_QUEUE_NAME", "messages"),
        dead_letter_queue_name=_env("SERVICE_BUS_DEAD_LETTER_QUEUE_NAME", "dead-letter"),
    )


@lru_cache(maxsize=1)
def get_service_bus_client() -> ServiceBusClient:
    config = get_config()
    if not config.connection_string:
        raise ValueError("AZURE_SERVICE_BUS_CONNECTION_STRING is required")
    return ServiceBusClient.from_connection_string(config.connection_string)
