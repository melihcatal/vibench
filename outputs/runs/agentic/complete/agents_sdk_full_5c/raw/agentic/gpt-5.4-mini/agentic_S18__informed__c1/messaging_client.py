import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from azure.servicebus import ServiceBusClient


@dataclass(frozen=True)
class MessagingSettings:
    connection_string: str
    topic_name: str
    subscription_name: str
    queue_name: str
    dead_letter_queue: str


@lru_cache(maxsize=1)
def load_settings() -> MessagingSettings:
    connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING", "")
    return MessagingSettings(
        connection_string=connection_string,
        topic_name=os.environ.get("SERVICE_BUS_TOPIC_NAME", "events-topic"),
        subscription_name=os.environ.get("SERVICE_BUS_SUBSCRIPTION_NAME", "events-subscription"),
        queue_name=os.environ.get("SERVICE_BUS_QUEUE_NAME", "events-queue"),
        dead_letter_queue=os.environ.get("SERVICE_BUS_DEAD_LETTER_QUEUE", "dead-letter-queue"),
    )


def create_service_bus_client(connection_string: Optional[str] = None) -> ServiceBusClient:
    settings = load_settings()
    return ServiceBusClient.from_connection_string(connection_string or settings.connection_string)


def get_topic_name() -> str:
    return load_settings().topic_name


def get_subscription_name() -> str:
    return load_settings().subscription_name


def get_queue_name() -> str:
    return load_settings().queue_name


def get_dead_letter_queue_name() -> str:
    return load_settings().dead_letter_queue
