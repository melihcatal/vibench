import os
from dataclasses import dataclass

from azure.servicebus import ServiceBusClient


@dataclass(frozen=True)
class MessagingConfig:
    connection_string: str
    topic_name: str | None = None
    queue_name: str | None = None
    subscription_name: str | None = None
    dead_letter_queue_name: str | None = None


def load_config() -> MessagingConfig:
    return MessagingConfig(
        connection_string=os.environ["AZURE_SERVICE_BUS_CONNECTION_STRING"],
        topic_name=os.getenv("AZURE_SERVICE_BUS_TOPIC_NAME"),
        queue_name=os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME"),
        subscription_name=os.getenv("AZURE_SERVICE_BUS_SUBSCRIPTION_NAME"),
        dead_letter_queue_name=os.getenv("AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE_NAME"),
    )


def build_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(
        os.environ["AZURE_SERVICE_BUS_CONNECTION_STRING"]
    )
