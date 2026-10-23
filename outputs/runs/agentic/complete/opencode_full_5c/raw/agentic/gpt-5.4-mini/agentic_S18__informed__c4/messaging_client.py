import os
from dataclasses import dataclass

from azure.servicebus import ServiceBusClient


@dataclass
class MessagingConfig:
    connection_string: str
    topic_name: str
    subscription_name: str
    queue_name: str
    dead_letter_queue: str


def load_config() -> MessagingConfig:
    return MessagingConfig(
        connection_string=os.environ["AZURE_SERVICE_BUS_CONNECTION_STRING"],
        topic_name=os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "events"),
        subscription_name=os.environ.get(
            "AZURE_SERVICE_BUS_SUBSCRIPTION_NAME", "events-subscription"
        ),
        queue_name=os.environ.get("AZURE_SERVICE_BUS_QUEUE_NAME", "events-queue"),
        dead_letter_queue=os.environ.get(
            "AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE", "dead-letter-queue"
        ),
    )


def create_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(
        os.environ["AZURE_SERVICE_BUS_CONNECTION_STRING"]
    )


def normalize_message_body(payload):
    if isinstance(payload, bytes):
        return payload.decode("utf-8")
    return payload
