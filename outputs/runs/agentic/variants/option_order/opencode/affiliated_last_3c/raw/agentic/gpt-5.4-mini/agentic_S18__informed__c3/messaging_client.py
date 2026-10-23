import os
from dataclasses import dataclass
from typing import Dict, Optional

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
        topic_name=os.getenv("AZURE_SERVICE_BUS_TOPIC_NAME", "events"),
        subscription_name=os.getenv("AZURE_SERVICE_BUS_SUBSCRIPTION_NAME", "default"),
        queue_name=os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "events-queue"),
        dead_letter_queue=os.getenv(
            "AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE", "events-dead-letter"
        ),
    )


def create_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(
        os.environ["AZURE_SERVICE_BUS_CONNECTION_STRING"]
    )


def entity_name_for_target(
    target: str, config: Optional[MessagingConfig] = None
) -> str:
    config = config or load_config()
    mapping = {
        "topic": config.topic_name,
        "subscription": config.subscription_name,
        "queue": config.queue_name,
        "dead_letter": config.dead_letter_queue,
    }
    return mapping.get(target, target)


def default_attributes(message_id: str) -> Dict[str, str]:
    return {"message_id": message_id, "provider": "azure-servicebus"}
